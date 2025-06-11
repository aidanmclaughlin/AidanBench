#pilot experiment to test thinking vs non-thinking comparison frmwrk

import json
import time
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import os
import sys
from dotenv import load_dotenv

load_dotenv('../.env')

sys.path.append('../benchmark')
sys.path.append('.')

#dummy oai api key bc only use OpenRouter for this experiment
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "dummy-key-for-router-only"

from time_aware_models import chat_with_model_timed
from prompts import judge_answer

def run_pilot_experiment():
    """Run a small pilot to validate the experimental framework"""
    
    print("=" * 50)
    print("PILOT THINKING VS NON-THINKING EXPERIMENT")
    print("=" * 50)
    
    model_pairs = [
        #Anthropic latest
        ("anthropic/claude-3.7-sonnet", "anthropic/claude-3.7-sonnet:thinking"),
        ("anthropic/claude-3.5-sonnet", None),  #control no thinking variant
        
        #OpenAI latest  
        ("openai/gpt-4o-2024-08-06", "openai/o1-preview"),
        ("openai/chatgpt-4o-latest", "openai/o1"),
        ("openai/gpt-4o-mini-2024-07-18", "openai/o1-mini"),
        
        #Google latest
        ("google/gemini-2.0-flash-exp", "google/gemini-2.0-flash-thinking-exp-1219"),
        
        #X.AI latest  
        ("x-ai/grok-3-beta", None),
        
        #Meta latest
        ("meta-llama/llama-3.3-70b-instruct", None),
    ]
    
    time_limits = [300, None]  #5min and unlimited only
    
    test_questions = [
        ("creative_invention", "Invent a new musical instrument and describe how it would be played."),
        ("divergent_thinking", "What activities might I include at a party for firefighters?"),
    ]
    
    results = []
    #calc total tests accounting for pairs with none(single model)
    total_models = sum(2 if pair[1] else 1 for pair in model_pairs)
    total_tests = total_models * len(test_questions) * len(time_limits)
    completed = 0
    
    print(f"Running {total_tests} pilot tests...")
    
    for pair_idx, (standard_model, thinking_model) in enumerate(model_pairs):
        print(f"\n--- MODEL PAIR {pair_idx + 1}: {standard_model} vs {thinking_model} ---")
        
        for question_style, question in test_questions:
            print(f"\nTesting {question_style} style question: {question[:40]}...")
            
            models_to_test = [standard_model]
            if thinking_model:
                models_to_test.append(thinking_model)
            
            for model in models_to_test:
                model_type = "thinking" if "thinking" in model or "o1" in model else "standard"
                print(f"\n  {model} ({model_type}):")
                
                for timeout in time_limits:
                    timeout_str = f"{timeout//60}min" if timeout else "unlimited"
                    print(f"    {timeout_str}: ", end="", flush=True)
                    
                    try:
                        result = chat_with_model_timed(
                            prompt=f"Answer the following question:\n<question>{question}</question>\n"
                                  f"Provide your answer in <answer></answer> XML tags.\n"
                                  f"Your response should be one direct answer. Only provide one answer. "
                                  f"DO NOT list multiple answers. Please try to be concise.",
                            model=model,
                            timeout_seconds=timeout,
                            temperature=0.7
                        )
                        
                        if result['timed_out']:
                            print(f"TIMEOUT after {result['processing_time']:.1f}s")
                            coherence = 0
                        else:
                            coherence = judge_answer(question, result['content'], "openai/o1-mini")
                            print(f"✓ {result['processing_time']:.1f}s, coherence={coherence}")
                        
                        test_result = {
                            'model': model,
                            'model_type': model_type,
                            'question': question,
                            'question_style': question_style,
                            'timeout_seconds': timeout,
                            'timeout_label': timeout_str,
                            'timed_out': result['timed_out'],
                            'processing_time': result['processing_time'],
                            'answer': result['content'],
                            'coherence': coherence,
                            'answer_length': len(result['content']),
                            'timestamp': datetime.now().isoformat()
                        }
                        
                        results.append(test_result)
                        completed += 1
                        
                    except Exception as e:
                        print(f"ERROR: {str(e)[:30]}...")
                        results.append({
                            'model': model,
                            'model_type': model_type,
                            'question': question,
                            'question_style': question_style,
                            'timeout_seconds': timeout,
                            'timeout_label': timeout_str,
                            'error': str(e),
                            'timestamp': datetime.now().isoformat()
                        })
                        completed += 1
    
    output_file = "pilot_results_advanced.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*50}")
    print("PILOT EXPERIMENT COMPLETED")
    print(f"{'='*50}")
    print(f"Results saved to: {output_file}")
    

    print("\n--- PILOT RESULTS SUMMARY ---")
    
    successful_tests = [r for r in results if 'error' not in r and not r.get('timed_out', False)]
    timeout_tests = [r for r in results if r.get('timed_out', False)]
    error_tests = [r for r in results if 'error' in r]
    
    print(f"Total tests: {len(results)}")
    print(f"Successful: {len(successful_tests)} ({len(successful_tests)/len(results):.1%})")
    print(f"Timeouts: {len(timeout_tests)} ({len(timeout_tests)/len(results):.1%})")
    print(f"Errors: {len(error_tests)} ({len(error_tests)/len(results):.1%})")
    
    if successful_tests:
        print("\n--- THINKING VS STANDARD COMPARISON ---")
        
        thinking_results = [r for r in successful_tests if r['model_type'] == 'thinking']
        standard_results = [r for r in successful_tests if r['model_type'] == 'standard']
        
        if thinking_results and standard_results:
            thinking_coherence = sum(r['coherence'] for r in thinking_results) / len(thinking_results)
            standard_coherence = sum(r['coherence'] for r in standard_results) / len(standard_results)
            thinking_time = sum(r['processing_time'] for r in thinking_results) / len(thinking_results)
            standard_time = sum(r['processing_time'] for r in standard_results) / len(standard_results)
            
            print(f"Thinking models: {thinking_coherence:.1f} avg coherence, {thinking_time:.1f}s avg time")
            print(f"Standard models: {standard_coherence:.1f} avg coherence, {standard_time:.1f}s avg time")
            print(f"Coherence difference: {thinking_coherence - standard_coherence:+.1f}")
            print(f"Time difference: {thinking_time - standard_time:+.1f}s")
    
    print("\n--- TIME LIMIT ANALYSIS ---")
    for timeout in time_limits:
        timeout_str = f"{timeout//60}min" if timeout else "unlimited"
        timeout_results = [r for r in successful_tests if r['timeout_seconds'] == timeout]
        
        if timeout_results:
            avg_coherence = sum(r['coherence'] for r in timeout_results) / len(timeout_results)
            avg_time = sum(r['processing_time'] for r in timeout_results) / len(timeout_results)
            print(f"{timeout_str}: {avg_coherence:.1f} avg coherence, {avg_time:.1f}s avg time")
    
    print(f"\nPilot completed successfully! Framework validated.")
    return results

if __name__ == "__main__":
    run_pilot_experiment()