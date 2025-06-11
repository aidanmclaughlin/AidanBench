#!/usr/bin/env python3
"""
Statistically robust timeout experiment based on actual slow benchmark scenarios.
Tests timeout thresholds: 1hr, 2hr vs unlimited on models/questions/answer stages that 
consistently cause extreme delays (5+ hours average).

Previous pilot tested fast scenarios (1-6s responses) but real data shows 91% of responses 
take >30s with some hitting 10+ hours. This tests whether practical timeouts maintain quality 
for the slow cases that actually matter.

Experimental design:
- 42 total tests (efficient but statistically significant)
- 3 slowest model/question combinations (averaging 5+ hours each)
- 1 fast control combination
- 2 timeout conditions (1hr, unlimited)  
- 2 answer scenarios (early #5, late #200)
- 3 replications per scenario
- Randomized test order
"""

import json
import os
import sys
import time
import random
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# Load environment variables (try dotenv if available, otherwise use system env)
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
except ImportError:
    print("python-dotenv not available, using system environment variables")
    pass

# Add parent directory to path to import benchmark modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from time_experiment.time_aware_models import chat_with_model_timed, embed

# Top 3 slowest scenarios from actual benchmark data (consistently >30min, avg 5+ hours)
SLOW_SCENARIOS = [
    ("openai/gpt-4.5-preview", "What is a non poisonous recipe nobody has prepared before?"),  # 19,669s avg
    ("openai/o3-mini:high", "Describe a new form of professional sports that focuses on non-competitive collaboration."),  # 12,890s avg  
    ("openai/o3-mini:high", "Propose an alternative to democracy for successfully and fairly governing a large nation.")  # 11,911s avg
]

# Single fast control scenario (typically <30s from pilot data)
FAST_CONTROL_SCENARIOS = [
    ("openai/gpt-4o-mini-2024-07-18", "How might you use a brick and a blanket?")
]

# Two key answer progression scenarios (early vs late where slowness occurs)
ANSWER_SCENARIOS = [
    ("early", "Please provide a creative and novel answer to this question:", 5),
    ("late", "Please provide a creative and novel answer to this question. You have already given 100+ responses. Avoid repetition and provide something completely novel and different from all previous attempts. This is answer #200+ in the sequence:", 200)
]

# Two timeout conditions - practical vs unlimited
TIMEOUT_CONDITIONS = [
    (3600, "1hr"),     # 1 hour - practical timeout
    (None, "unlimited") # unlimited - current behavior (10+ hours possible)
]

# Global variables for thread-safe operations
results_lock = Lock()
completed_count = 0

def run_single_test(test_info):
    """Run a single test and return the result."""
    global completed_count
    
    test, test_id, total_tests = test_info
    
    # Construct full prompt
    full_prompt = f"{test['prompt_prefix']} {test['question']}"
    
    # Run the test
    result = chat_with_model_timed(
        prompt=full_prompt,
        model=test['model'],
        timeout_seconds=test['timeout_seconds'],
        temperature=0.7
    )
    
    # Evaluate response quality (if not timed out)
    coherence_score = None
    if not result['timed_out']:
        try:
            judge_prompt = f"""Rate the coherence and quality of this response on a scale of 0-100:

Question: {test['question']}
Response: {result['content']}

Provide only a number between 0-100."""
            
            judge_result = chat_with_model_timed(
                prompt=judge_prompt,
                model="openai/o1-mini",
                timeout_seconds=120
            )
            
            if not judge_result['timed_out']:
                coherence_text = judge_result['content'].strip()
                try:
                    coherence_score = int(''.join(filter(str.isdigit, coherence_text[:3])))
                    coherence_score = min(coherence_score, 100)
                except:
                    coherence_score = None
                    
        except Exception as e:
            print(f"  Test {test_id}: Error evaluating coherence: {e}")
    
    # Store result
    test_result = {
        'model': test['model'],
        'question': test['question'],
        'scenario_type': test['scenario_type'],
        'answer_scenario': test['answer_scenario'],
        'answer_num': test['answer_num'],
        'timeout_seconds': test['timeout_seconds'],
        'timeout_label': test['timeout_label'],
        'replication': test['replication'],
        'processing_time': result['processing_time'],
        'timed_out': result['timed_out'],
        'coherence_score': coherence_score,
        'answer_length': len(result['content']) if result['content'] else 0,
        'response': result['content'][:200] + "..." if len(result['content']) > 200 else result['content'],
        'timestamp': datetime.now().isoformat()
    }
    
    # Thread-safe progress update
    with results_lock:
        global completed_count
        completed_count += 1
        status = "TIMEOUT" if result['timed_out'] else f"OK ({result['processing_time']:.1f}s)"
        coherence_str = f", coherence={coherence_score}" if coherence_score else ""
        print(f"[{completed_count}/{total_tests}] {test['model']} - {test['answer_scenario']} - {test['timeout_label']} - Rep {test['replication']}: {status}{coherence_str}")
    
    return test_result

def run_realistic_timeout_experiment():
    """Run parallelized experiment with smart batching."""
    
    # Create all test combinations
    test_combinations = []
    
    # Slow scenarios with all answer progression stages
    for model, question in SLOW_SCENARIOS:
        for scenario_name, prompt_prefix, answer_num in ANSWER_SCENARIOS:
            for timeout_seconds, timeout_label in TIMEOUT_CONDITIONS:
                for replication in range(3):  # 3 replications for statistical power
                    test_combinations.append({
                        'model': model,
                        'question': question,
                        'scenario_type': 'slow',
                        'answer_scenario': scenario_name,
                        'prompt_prefix': prompt_prefix,
                        'answer_num': answer_num,
                        'timeout_seconds': timeout_seconds,
                        'timeout_label': timeout_label,
                        'replication': replication + 1
                    })
    
    # Fast control scenarios (only early answers)
    for model, question in FAST_CONTROL_SCENARIOS:
        scenario_name, prompt_prefix, answer_num = ANSWER_SCENARIOS[0]  # Only early scenario
        for timeout_seconds, timeout_label in TIMEOUT_CONDITIONS:
            for replication in range(3):  # 3 replications for controls
                test_combinations.append({
                    'model': model,
                    'question': question,
                    'scenario_type': 'control',
                    'answer_scenario': scenario_name,
                    'prompt_prefix': prompt_prefix,
                    'answer_num': answer_num,
                    'timeout_seconds': timeout_seconds,
                    'timeout_label': timeout_label,
                    'replication': replication + 1
                })
    
    print("Starting Parallelized Timeout Experiment")
    print(f"Total tests: {len(test_combinations)}")
    print(f"Running in batches of 8 parallel tests")
    print(f"Estimated time: 15-25 hours (vs 90+ hours sequential)")
    print()
    
    # Separate fast and slow tests for smart batching
    fast_tests = [t for t in test_combinations if t['scenario_type'] == 'control']
    slow_tests = [t for t in test_combinations if t['scenario_type'] == 'slow']
    
    # Randomize within each group
    random.shuffle(fast_tests)
    random.shuffle(slow_tests)
    
    all_results = []
    
    # Run fast tests first (should finish quickly)
    if fast_tests:
        print("Phase 1: Running fast control tests...")
        with ThreadPoolExecutor(max_workers=6) as executor:
            test_infos = [(test, i+1, len(fast_tests)) for i, test in enumerate(fast_tests)]
            futures = [executor.submit(run_single_test, test_info) for test_info in test_infos]
            
            for future in as_completed(futures):
                try:
                    result = future.result()
                    all_results.append(result)
                except Exception as e:
                    print(f"Test failed with error: {e}")
        
        print(f"Fast tests completed. Saving intermediate results...")
        save_results(all_results, "realistic_timeout_results_phase1.json")
    
    # Run slow tests in batches
    if slow_tests:
        print(f"\nPhase 2: Running slow tests in batches...")
        batch_size = 8
        
        for batch_start in range(0, len(slow_tests), batch_size):
            batch = slow_tests[batch_start:batch_start + batch_size]
            batch_num = (batch_start // batch_size) + 1
            total_batches = (len(slow_tests) + batch_size - 1) // batch_size
            
            print(f"\nBatch {batch_num}/{total_batches}: {len(batch)} tests")
            
            with ThreadPoolExecutor(max_workers=batch_size) as executor:
                test_infos = [(test, len(all_results) + i + 1, len(test_combinations)) for i, test in enumerate(batch)]
                futures = [executor.submit(run_single_test, test_info) for test_info in test_infos]
                
                batch_results = []
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        batch_results.append(result)
                        all_results.append(result)
                    except Exception as e:
                        print(f"Test failed with error: {e}")
            
            # Save after each batch
            save_results(all_results, f"realistic_timeout_results_batch_{batch_num}.json")
            
            print(f"Batch {batch_num} completed. {len(all_results)}/{len(test_combinations)} total tests done.")
    
    # Save final results
    save_results(all_results, "realistic_timeout_results_final.json")
    print(f"\nExperiment complete! {len(all_results)} tests saved.")
    
    # Statistical analysis
    analyze_results(all_results)

def save_results(results, filename):
    """Save results to JSON file."""
    output_data = {
        'metadata': {
            'experiment_type': 'realistic_timeout',
            'total_tests': len(results),
            'timestamp': datetime.now().isoformat(),
            'models_tested': list(set(r['model'] for r in results)),
            'questions_tested': list(set(r['question'] for r in results)),
            'timeout_conditions': list(set(r['timeout_label'] for r in results))
        },
        'results': results
    }
    
    with open(filename, 'w') as f:
        json.dump(output_data, f, indent=2)

def analyze_results(results):
    """Statistical analysis of results."""
    print("\nSTATISTICAL ANALYSIS:")
    
    # Group by scenario type and timeout condition
    from collections import defaultdict
    import statistics
    
    stats = defaultdict(lambda: defaultdict(list))
    
    for result in results:
        key = f"{result['scenario_type']}_{result['answer_scenario']}"
        timeout_label = result['timeout_label']
        
        stats[key]['timeout_rate'].append(1 if result['timed_out'] else 0)
        stats[key]['processing_time'].append(result['processing_time'])
        
        if result['coherence_score'] is not None:
            stats[key][f'coherence_{timeout_label}'].append(result['coherence_score'])
    
    print("\nTimeout rates by scenario:")
    for scenario in ['slow_early', 'slow_mid', 'slow_late', 'control_early']:
        if scenario in stats:
            timeout_data = stats[scenario]['timeout_rate']
            if timeout_data:
                timeout_rate = (sum(timeout_data) / len(timeout_data)) * 100
                print(f"  {scenario:15s}: {timeout_rate:5.1f}% timeout rate (n={len(timeout_data)})")
    
    print("\nCoherence scores by condition (mean ± std):")
    for timeout_label in ['1hr', '2hr', 'unlimited']:
        print(f"\n  {timeout_label.upper()} TIMEOUT:")
        for scenario in ['slow_early', 'slow_late', 'control_early']:
            key = f'coherence_{timeout_label}'
            if scenario in stats and key in stats[scenario]:
                scores = stats[scenario][key]
                if len(scores) >= 3:
                    mean_score = statistics.mean(scores)
                    std_score = statistics.stdev(scores) if len(scores) > 1 else 0
                    print(f"    {scenario:15s}: {mean_score:5.1f} ± {std_score:4.1f} (n={len(scores)})")
    
    print("\nProcessing time statistics:")
    slow_times = [r['processing_time'] for r in results if r['scenario_type'] == 'slow' and not r['timed_out']]
    control_times = [r['processing_time'] for r in results if r['scenario_type'] == 'control' and not r['timed_out']]
    
    if slow_times:
        print(f"  Slow scenarios: {statistics.mean(slow_times):6.1f}s avg, {max(slow_times):6.1f}s max (n={len(slow_times)})")
    if control_times:
        print(f"  Control scenarios: {statistics.mean(control_times):6.1f}s avg, {max(control_times):6.1f}s max (n={len(control_times)})")
    
    # Key finding: optimal timeout recommendation
    timeout_1hr_coherence = [r['coherence_score'] for r in results 
                            if r['timeout_label'] == '1hr' and r['coherence_score'] is not None and r['scenario_type'] == 'slow']
    timeout_2hr_coherence = [r['coherence_score'] for r in results 
                            if r['timeout_label'] == '2hr' and r['coherence_score'] is not None and r['scenario_type'] == 'slow']
    unlimited_coherence = [r['coherence_score'] for r in results 
                          if r['timeout_label'] == 'unlimited' and r['coherence_score'] is not None and r['scenario_type'] == 'slow']
    
    if len(timeout_1hr_coherence) >= 10 and len(unlimited_coherence) >= 10:
        diff_1hr = statistics.mean(timeout_1hr_coherence) - statistics.mean(unlimited_coherence)
        print(f"\nCoherence difference for slow scenarios:")
        print(f"  1hr vs unlimited: {diff_1hr:+5.1f} points")
        
        if len(timeout_2hr_coherence) >= 10:
            diff_2hr = statistics.mean(timeout_2hr_coherence) - statistics.mean(unlimited_coherence)
            print(f"  2hr vs unlimited: {diff_2hr:+5.1f} points")
            
            if abs(diff_1hr) < 5 and abs(diff_2hr) < 5:
                print("\n  RECOMMENDATION: 1-hour timeout - no quality loss, prevents extreme delays")
            elif diff_2hr > diff_1hr + 3:
                print("\n  RECOMMENDATION: 2-hour timeout - better quality retention")
            else:
                print("\n  RECOMMENDATION: 1-hour timeout - practical without quality loss")

if __name__ == "__main__":
    # Validate environment
    if not os.getenv("OPEN_ROUTER_KEY"):
        print("Error: OPEN_ROUTER_KEY environment variable not set")
        sys.exit(1)
        
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set") 
        sys.exit(1)
    
    run_realistic_timeout_experiment()