from openai import OpenAI
import os
from functools import lru_cache
from retry import retry


@retry()
def chat_with_model(prompt: str, model: str, max_tokens: int = 4000, temperature: float = 0) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


@lru_cache(maxsize=10000)
@retry(tries=3)
def embed(text: str) -> list[float]:
    model_name = "text-embedding-3-large"
    client = OpenAI()
    response = client.embeddings.create(
        model=model_name, input=[text])
    return response.data[0].embedding
