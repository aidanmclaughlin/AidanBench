#seeing if time limits affect the quality of the openended responses
#do reasoning models benefit from unlimited time or can i find an optimal time window etc
#5min vs unlimited time limit for questions

from openai import OpenAI
import os
import time
import signal
from functools import lru_cache
from retry import retry
from contextlib import contextmanager


#client for OpenRouter for chat completions
router_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPEN_ROUTER_KEY")
)

#client for oai for embeddings
openai_client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

class TimeoutError(Exception):
    pass

#using unix sigalrm to interrupt the long api calls; so time expires the timeouterror gets raised and then breaks the api request
@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutError(f"Request timed out after {seconds} seconds")
    
    old_handler = signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)

@retry(tries=3, delay=1, backoff=2) #retrying function calls for if api calls fails, just didnt want manual retry logic
def chat_with_model_timed(prompt: str, model: str, max_tokens: int = 4000, temperature: float = 0, timeout_seconds: int = None) -> dict:
    """making the api call, with limits, returning dict of response, processing time, timeout stuff etc"""
    start_time = time.time()
    
    params = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature
    }
    
    try:
        if timeout_seconds:
            with time_limit(timeout_seconds):
                response = router_client.chat.completions.create(**params)
        else:
            response = router_client.chat.completions.create(**params)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        return {
            'content': response.choices[0].message.content,
            'processing_time': processing_time,
            'timed_out': False,
            'timeout_limit': timeout_seconds
        }
        
    except TimeoutError as e:
        end_time = time.time()
        processing_time = end_time - start_time
        
        return {
            'content': f"[TIMEOUT] Response exceeded {timeout_seconds} second limit",
            'processing_time': processing_time,
            'timed_out': True,
            'timeout_limit': timeout_seconds
        }

@lru_cache(maxsize=10000)
@retry(tries=3, delay=1, backoff=2)
def embed(text: str) -> list[float]:
    model_name = "text-embedding-3-large"
    response = openai_client.embeddings.create(
        model=model_name, input=[text])
    return response.data[0].embedding