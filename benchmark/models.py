from openai import OpenAI
import os
from functools import lru_cache
from retry import retry


# Create client for OpenRouter (for chat completions)
router_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPEN_ROUTER_KEY")
)

# Create client for OpenAI (for embeddings)
openai_client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

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
    
    response = router_client.chat.completions.create(**params)
    return response.choices[0].message.content


@lru_cache(maxsize=10000)
@retry(tries=3, delay=1, backoff=2)
def embed(text: str) -> list[float]:
    model_name = "text-embedding-3-large"
    response = openai_client.embeddings.create(
        model=model_name, input=[text])
    return response.data[0].embedding
