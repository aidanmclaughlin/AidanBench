#so how long do the models actually take...

import json
import time
from time_aware_prompts import gen_answer_with_time_limit

MODELS_TO_TIME = [
    #fast standard models
    "openai/gpt-4o-mini-2024-07-18",
    "anthropic/claude-3.5-sonnet", 
    
    #reasoning models  
    "openai/o1-mini",
    "openai/o1-preview",
    
    #thinking variants
    "anthropic/claude-3.7-sonnet",
    "anthropic/claude-3.7-sonnet:thinking",
    
    #hybrid reasoning
    "x-ai/grok-3-mini-beta:medium",
    "google/gemini-2.0-flash-thinking-exp-1219"
]

SAMPLE_QUESTIONS = [
    "How might you use a brick and a blanket?",
    "Propose a solution to Los Angeles traffic.",
    "Invent a new musical instrument and describe how it would be played."
]

timing_results = []

print("=== TIMING BASELINE EXPERIMENT ===")
print("Testing how long each model type actually takes (no time limits)")

for model in MODELS_TO_TIME:
    print(f"\n--- Testing {model} ---")
    model_times = []
    
    for question in SAMPLE_QUESTIONS:
        print(f"  {question[:30]}...", end=" ")
        
        try:
            start_time = time.time()
            result = gen_answer_with_time_limit(question, [], model, timeout_seconds=None)
            
            data = {
                'model': model,
                'question': question,
                'processing_time': result['processing_time'],
                'answer_length': len(result['answer']),
                'timed_out': result['timed_out']
            }
            
            timing_results.append(data)
            model_times.append(result['processing_time'])
            
            print(f"{result['processing_time']:.1f}s")
            
        except Exception as e:
            print(f"ERROR: {str(e)[:30]}")
            timing_results.append({
                'model': model,
                'question': question, 
                'error': str(e)
            })
    
    if model_times:
        avg_time = sum(model_times) / len(model_times)
        max_time = max(model_times)
        min_time = min(model_times)
        print(f"  → {model}: avg={avg_time:.1f}s, range={min_time:.1f}-{max_time:.1f}s")

with open('timing_baseline.json', 'w') as f:
    json.dump(timing_results, f, indent=2)


print(f"\n=== TIMING ANALYSIS ===")

model_categories = {
    'Fast Standard': ['gpt-4o-mini', 'claude-3.5-sonnet'],
    'Reasoning': ['o1-mini', 'o1-preview'], 
    'Thinking': ['claude-3.7-sonnet:thinking', 'gemini-2.0-flash-thinking'],
    'Non-Thinking': ['claude-3.7-sonnet'],
    'Hybrid': ['grok-3-mini-beta']
}

for category, model_patterns in model_categories.items():
    category_times = []
    for result in timing_results:
        if 'processing_time' in result:
            model = result['model']
            if any(pattern in model for pattern in model_patterns):
                category_times.append(result['processing_time'])
    
    if category_times:
        avg_time = sum(category_times) / len(category_times)
        max_time = max(category_times)
        print(f"{category:15}: avg={avg_time:5.1f}s, max={max_time:5.1f}s ({len(category_times)} samples)")

print(f"\nTiming baseline completed! Results saved to timing_baseline.json")