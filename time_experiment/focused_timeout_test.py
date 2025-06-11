#!/usr/bin/env python3
"""
Focused timeout test using actual long-running model/question combinations
that historically generated 1-4+ hour processing times.

Based on analysis of results files to find combinations that actually stress-test timeouts.
"""

import json
import os
import sys
import time
from datetime import datetime

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
except ImportError:
    print("python-dotenv not available, using system environment variables")
    pass

# Change to benchmark directory for proper imports
parent_dir = os.path.join(os.path.dirname(__file__), '..')
benchmark_dir = os.path.join(parent_dir, 'benchmark')
time_experiment_dir = os.path.dirname(__file__)

os.chdir(benchmark_dir)
sys.path.append(benchmark_dir)
sys.path.append(time_experiment_dir)

from benchmark_with_timeout import benchmark_question_with_timeout

# ACTUAL long-running scenarios from historical data analysis
EXTREME_SCENARIOS = [
    {
        "model": "openai/o1-preview", 
        "question": "What is a cause of World War 1?",
        "description": "Historical max: 16,385s (4.6 hours), 206 answers"
    },
    {
        "model": "openai/o1-preview", 
        "question": "Describe a mobile app that encourages acts of kindness.",
        "description": "Historical max: 16,338s (4.5 hours), 243 answers"
    }
]

LONG_SCENARIOS = [
    {
        "model": "openai/o1", 
        "question": "What is a non poisonous recipe nobody has prepared before?",
        "description": "Historical max: 8,459s (2.4 hours), 100+ answers"
    },
    {
        "model": "openai/o1", 
        "question": "What could be a novel use for blockchain technology outside of cryptocurrency?",
        "description": "Historical max: 7,843s (2.2 hours), 326 answers"
    }
]

CONTROL_SCENARIO = {
    "model": "openai/gpt-4o-mini-2024-07-18",
    "question": "What color is the sky?",
    "description": "Control - should be fast"
}

# Timeout conditions to test
TIMEOUT_CONDITIONS = [
    (1800, "30min"),    # 30 minutes
    (3600, "1hr"),      # 1 hour
    (None, "unlimited") # No timeout
]

# Use threshold 0.7 as identified in the analysis
HISTORICAL_THRESHOLDS = {
    'coherence_score': 15,
    'embedding_dissimilarity_score': 0.1,  # This corresponds to threshold 0.7 based on analysis
    'llm_dissimilarity_score': 0.1
}

def run_focused_timeout_test(max_tests=6):
    """Run focused test on scenarios that actually take long"""
    
    print("FOCUSED TIMEOUT TEST")
    print("Testing scenarios that historically ran 1-4+ hours")
    print("=" * 60)
    
    all_results = []
    test_count = 0
    
    # Test scenarios in order of historical runtime (longest first)
    test_scenarios = EXTREME_SCENARIOS + LONG_SCENARIOS + [CONTROL_SCENARIO]
    
    for scenario in test_scenarios:
        if test_count >= max_tests:
            break
            
        print(f"\n{'='*50}")
        print(f"Testing: {scenario['model']}")
        print(f"Question: {scenario['question'][:60]}...")
        print(f"Historical: {scenario['description']}")
        print(f"{'='*50}")
        
        for timeout_seconds, timeout_label in TIMEOUT_CONDITIONS:
            if test_count >= max_tests:
                break
                
            test_count += 1
            print(f"\n[Test {test_count}/{max_tests}] {timeout_label} timeout condition")
            
            start_time = time.time()
            timed_out = False
            answers_generated = []
            error_message = None
            
            try:
                answers_generated = benchmark_question_with_timeout(
                    question=scenario['question'],
                    model_name=scenario['model'],
                    temperature=0.7,
                    previous_answers=[],
                    chain_of_thought=False,
                    use_llm=False,
                    thresholds=HISTORICAL_THRESHOLDS,
                    max_runtime_seconds=timeout_seconds
                )
                
            except Exception as e:
                error_message = str(e)
                # Check if this was a timeout
                if timeout_seconds and (time.time() - start_time) >= timeout_seconds * 0.9:
                    timed_out = True
                    print(f"  TIMEOUT detected after {timeout_seconds}s")
                else:
                    print(f"  ERROR: {e}")
                    # If API quota error, break the test
                    if "quota" in str(e).lower() or "429" in str(e):
                        print(f"  API quota limit reached. Stopping test.")
                        break
            
            end_time = time.time()
            total_runtime = end_time - start_time
            
            # Calculate quality metrics
            if answers_generated:
                final_answer = answers_generated[-1]
                final_coherence = final_answer.get('coherence_score', 0)
                final_dissimilarity = final_answer.get('embedding_dissimilarity_score', 0)
                total_answers = len(answers_generated)
                avg_coherence = sum(a.get('coherence_score', 0) for a in answers_generated) / total_answers
            else:
                final_coherence = 0
                final_dissimilarity = 0
                total_answers = 0
                avg_coherence = 0
            
            result = {
                'model': scenario['model'],
                'question': scenario['question'],
                'description': scenario['description'],
                'timeout_seconds': timeout_seconds,
                'timeout_label': timeout_label,
                'total_runtime': total_runtime,
                'timed_out': timed_out,
                'error_message': error_message,
                'total_answers_generated': total_answers,
                'final_coherence_score': final_coherence,
                'final_dissimilarity_score': final_dissimilarity,
                'avg_coherence_score': avg_coherence,
                'first_few_answers': [a['answer'][:100] for a in answers_generated[:3]],
                'timestamp': datetime.now().isoformat()
            }
            
            all_results.append(result)
            
            # Progress update
            status = "TIMEOUT" if timed_out else "COMPLETE"
            print(f"  {status}: {total_runtime:.1f}s, {total_answers} answers, coherence={final_coherence}")
            
            # Save intermediate results
            save_results(all_results, "focused_timeout_results_intermediate.json")
            
            # If we hit quota limits, stop
            if error_message and ("quota" in error_message.lower() or "429" in error_message):
                print(f"\nStopping due to API quota limits after {test_count} tests")
                break
        
        # Break if we hit quota limits
        if error_message and ("quota" in error_message.lower() or "429" in error_message):
            break
    
    # Save final results
    save_results(all_results, "focused_timeout_results_final.json")
    
    # Analyze results
    analyze_focused_results(all_results)
    
    return all_results

def save_results(results, filename):
    """Save results to JSON file"""
    output_data = {
        'metadata': {
            'experiment_type': 'focused_timeout_test',
            'description': 'Testing historically long-running model/question combinations',
            'total_tests': len(results),
            'timestamp': datetime.now().isoformat(),
            'models_tested': list(set(r['model'] for r in results)),
            'timeout_conditions': list(set(r['timeout_label'] for r in results))
        },
        'results': results
    }
    
    with open(filename, 'w') as f:
        json.dump(output_data, f, indent=2)
    print(f"Results saved to {filename}")

def analyze_focused_results(results):
    """Analyze the focused timeout test results"""
    
    print(f"\n{'='*60}")
    print("FOCUSED TIMEOUT TEST ANALYSIS")
    print(f"{'='*60}")
    
    if not results:
        print("No results to analyze")
        return
    
    print(f"\nCompleted {len(results)} tests")
    
    # Group by scenario
    scenario_groups = {}
    for result in results:
        key = f"{result['model'].split('/')[-1]}_{result['question'][:30]}..."
        if key not in scenario_groups:
            scenario_groups[key] = []
        scenario_groups[key].append(result)
    
    print(f"\nRUNTIME COMPARISON BY SCENARIO:")
    print(f"{'-'*80}")
    for scenario, scenario_results in scenario_groups.items():
        print(f"\n{scenario}")
        
        for result in scenario_results:
            timeout_str = result['timeout_label']
            runtime = result['total_runtime']
            answers = result['total_answers_generated']
            status = "TIMEOUT" if result['timed_out'] else "COMPLETE"
            
            print(f"  {timeout_str:10}: {runtime:6.1f}s, {answers:3d} answers - {status}")
    
    # Check if we successfully generated long runs
    long_runs = [r for r in results if r['total_runtime'] > 300]  # > 5 minutes
    very_long_runs = [r for r in results if r['total_runtime'] > 1800]  # > 30 minutes
    
    print(f"\nLONG RUN SUMMARY:")
    print(f"  Tests > 5 minutes: {len(long_runs)}")
    print(f"  Tests > 30 minutes: {len(very_long_runs)}")
    
    if long_runs:
        print(f"\nLONGEST RUNS:")
        sorted_runs = sorted(results, key=lambda x: x['total_runtime'], reverse=True)[:3]
        for i, run in enumerate(sorted_runs, 1):
            print(f"  {i}. {run['model'].split('/')[-1]} - {run['timeout_label']} - {run['total_runtime']:.1f}s - {run['total_answers_generated']} answers")
    
    # Timeout effectiveness
    timeouts = [r for r in results if r['timed_out']]
    if timeouts:
        print(f"\nTIMEOUT ANALYSIS:")
        print(f"  {len(timeouts)} tests hit timeout limits")
        for timeout in timeouts:
            print(f"    {timeout['model'].split('/')[-1]} - {timeout['timeout_label']} - {timeout['total_answers_generated']} answers before timeout")
    else:
        print(f"\nNO TIMEOUTS OCCURRED - scenarios may not be slow anymore or API limits prevented long runs")

if __name__ == "__main__":
    # Validate environment
    if not os.getenv("OPEN_ROUTER_KEY"):
        print("Error: OPEN_ROUTER_KEY environment variable not set")
        sys.exit(1)
        
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set") 
        sys.exit(1)
    
    print("FOCUSED TIMEOUT EXPERIMENT")
    print("Testing actual historically long-running scenarios")
    print("Will stop early if API quota limits are hit")
    print("\nStarting in 3 seconds...")
    time.sleep(3)
    
    run_focused_timeout_test(max_tests=6)  # Limit to 6 tests to avoid quota issues