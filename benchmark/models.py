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

@retry(tries=3, delay=1, backoff=2)
def chat_with_model(prompt: str, model: str, max_tokens: int = 4000, temperature: float = 0) -> str:
    # Default parameters for API call
    params = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    # Check if this is grok-3-mini-beta with reasoning effort specified
    if model.startswith("x-ai/grok-3-mini-beta:"):
        model_parts = model.split(":")
        if len(model_parts) == 2:
            base_model = model_parts[0]
            reasoning_effort = model_parts[1]
            
            # Only accept valid reasoning effort values
            if reasoning_effort in ["low", "medium", "high"]:
                params["model"] = base_model
                params["reasoning"] = {"effort": reasoning_effort}
    
    response = get_router_client().chat.completions.create(**params)
    return response.choices[0].message.content


@lru_cache(maxsize=10000)
@retry(tries=3, delay=1, backoff=2)
def embed(text: str) -> list[float]:
    model_name = "text-embedding-3-large"
    response = get_openai_client().embeddings.create(
        model=model_name, input=[text])
    return response.data[0].embedding
