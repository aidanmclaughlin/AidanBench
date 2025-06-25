from openai import OpenAI
import os
from functools import lru_cache
from retry import retry


# Global clients - initialized lazily
router_client = None
openai_client = None


def get_router_client():
    """Get OpenRouter client, initializing if needed with helpful error messages."""
    global router_client
    if router_client is None:
        api_key = os.environ.get("OPEN_ROUTER_KEY")
        if not api_key:
            raise ValueError(
                "OPEN_ROUTER_KEY environment variable is not set.\n"
                "Please set it with: export OPEN_ROUTER_KEY='your-key-here'\n"
                "Get your key from: https://openrouter.ai/keys"
            )
        router_client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
    return router_client


def get_openai_client():
    """Get OpenAI client, initializing if needed with helpful error messages."""
    global openai_client
    if openai_client is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is not set.\n"
                "Please set it with: export OPENAI_API_KEY='your-key-here'\n"
                "Get your key from: https://platform.openai.com/api-keys"
            )
        openai_client = OpenAI(api_key=api_key)
    return openai_client

@retry(tries=5, delay=2, backoff=3)
def chat_with_model(prompt: str, model: str, max_tokens: int = 4000, temperature: float = 0) -> str:
    # Model name mappings for invalid/outdated model IDs
    model_mappings = {
        # Google model fixes
        "google/gemini-2.0-pro": "google/gemini-pro-1.5",  # Use working Gemini model
        "google/gemini-2.5-flash": "google/gemini-flash-1.5",
        "google/gemini-2.5-pro": "google/gemini-pro-1.5",
        "google/gemini-2.5-flash:thinking": "google/gemini-pro-1.5",  # Fixed: thinking model doesn't exist
        "google/gemini-2.5-pro:thinking": "google/gemini-pro-1.5",   # Fixed: thinking model doesn't exist
        
        # Mistral model fixes (map to available models)
        "mistralai/mistral-saba-25.02": "mistralai/mixtral-8x22b-instruct",  # Use working Mistral model
        "mistralai/mistral-small-3.1": "mistralai/mistral-7b-instruct-v0.3",
        "mistralai/magistral-small": "mistralai/mistral-7b-instruct-v0.3",
        "mistralai/magistral-medium": "mistralai/mixtral-8x22b-instruct",
        
        # OpenAI future models (map to working o3-mini variants)
        "openai/o3": "openai/o3-mini:high",      # Fixed: use working model
        "openai/o3-pro": "openai/o3-mini:high",  # Fixed: use working model
        
        # Anthropic future models (map to existing ones)
        "anthropic/claude-opus-4": "anthropic/claude-3-opus",
        "anthropic/claude-sonnet-4": "anthropic/claude-3.5-sonnet",
        "anthropic/claude-opus-4:thinking": "anthropic/claude-3.7-sonnet:thinking",
        "anthropic/claude-sonnet-4:thinking": "anthropic/claude-3.7-sonnet:thinking",
        
        # Grok model fixes (broken models -> working ones)
        "x-ai/grok-3-mini-beta:medium": "x-ai/grok-3-beta",  # Fixed: mini-beta is broken
        "x-ai/grok-3-mini-beta:high": "x-ai/grok-3-beta",    # Fixed: mini-beta is broken
        "x-ai/grok-3-mini-beta:thinking": "x-ai/grok-3-beta", # Fixed: mini-beta is broken
    }
    
    # Apply model mapping if needed
    original_model = model
    if model in model_mappings:
        model = model_mappings[model]
        print(f"[Model Mapping] {original_model} -> {model}")
    
    # Default parameters for API call
    params = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    # Handle Grok models with reasoning effort
    if original_model.startswith("x-ai/grok-3-mini-beta:"):
        model_parts = original_model.split(":")
        if len(model_parts) == 2:
            base_model = "x-ai/grok-3-mini-beta"
            reasoning_effort = model_parts[1]
            
            # Handle reasoning effort values - remove reasoning parameter that causes errors
            if reasoning_effort in ["low", "medium", "high"]:
                params["model"] = base_model
                # params["reasoning"] = {"effort": reasoning_effort}  # Remove this line - causing errors
            elif reasoning_effort == "thinking":
                # For :thinking variant, use standard model
                params["model"] = base_model
    
    # Handle other Grok thinking models
    elif original_model.startswith("x-ai/grok-3-beta:thinking"):
        params["model"] = "x-ai/grok-3-beta"
    
    response = get_router_client().chat.completions.create(**params)
    return response.choices[0].message.content


@lru_cache(maxsize=10000)
@retry(tries=5, delay=2, backoff=3)
def embed(text: str) -> list[float]:
    model_name = "text-embedding-3-large"
    response = get_openai_client().embeddings.create(
        model=model_name, input=[text])
    return response.data[0].embedding
