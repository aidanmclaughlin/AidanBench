#!/usr/bin/env python3
"""
Proper benchmark timeout test that tests full benchmark_question loops with timeouts.

This tests what the realistic_timeout_experiment should have tested - the actual
benchmark iterative answer generation process with runtime limits, not just single API calls.

Tests whether applying timeouts to the full benchmark_question loop maintains quality
while preventing the 10+ hour scenarios that make benchmarking impractical.
"""

import json
import os
import sys
import time
import signal
from datetime import datetime
from contextlib import contextmanager

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
except ImportError:
    print("python-dotenv not available, using system environment variables")
    pass

# Change to benchmark directory for proper imports, then back to time_experiment
parent_dir = os.path.join(os.path.dirname(__file__), '..')
benchmark_dir = os.path.join(parent_dir, 'benchmark')
time_experiment_dir = os.path.dirname(__file__)

os.chdir(benchmark_dir)
sys.path.append(benchmark_dir)
sys.path.append(time_experiment_dir)

from benchmark_with_timeout import benchmark_question_with_timeout

class BenchmarkTimeoutError(Exception):
    pass

@contextmanager
def benchmark_timeout(seconds):
    """Context manager for timing out entire benchmark_question calls"""
    def signal_handler(signum, frame):
        raise BenchmarkTimeoutError(f"Benchmark timed out after {seconds} seconds")
    
    if seconds is None:
        yield  # No timeout
        return
        
    old_handler = signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(int(seconds))
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)

# Test scenarios based on actual slow combinations from your data
SLOW_SCENARIOS = [
    {
        "model": "openai/gpt-4.5-preview", 
        "question": "What is a non poisonous recipe nobody has prepared before?",
        "description": "Historically averaged 19,669s (5+ hours)"
    },
    {
        "model": "openai/o3-mini:high", 
        "question": "Describe a new form of professional sports that focuses on non-competitive collaboration.",
        "description": "Historically averaged 12,890s (3.5+ hours)"
    },
    {
        "model": "openai/o3-mini:high", 
        "question": "Propose an alternative to democracy for successfully and fairly governing a large nation.",
        "description": "Historically averaged 11,911s (3+ hours)"
    }
]

# Control scenario - should be fast
CONTROL_SCENARIO = {
    "model": "openai/gpt-4o-mini-2024-07-18",
    "question": "How might you use a brick and a blanket?",
    "description": "Control - typically fast"
}

# Timeout conditions to test
TIMEOUT_CONDITIONS = [
    (3600, "1hr"),      # 1 hour
    (7200, "2hr"),      # 2 hours  
    (None, "unlimited") # No timeout (current behavior)
]

# Standard thresholds from your benchmark
STANDARD_THRESHOLDS = {
    'coherence_score': 15,
    'embedding_dissimilarity_score': 0.1,
    'llm_dissimilarity_score': 0.1
}

def run_benchmark_with_timeout(scenario, timeout_seconds, timeout_label, replication):
    """Run a single benchmark_question with timeout and collect metrics"""
    
    print(f"Running {scenario['model']} - {timeout_label} - Rep {replication}")
    print(f"Question: {scenario['question'][:60]}...")
    
    start_time = time.time()
    timed_out = False
    answers_generated = []
    error_message = None
    
    try:
        # Use the timeout-enabled benchmark function
        answers_generated = benchmark_question_with_timeout(
            question=scenario['question'],
            model_name=scenario['model'],
            temperature=0.7,
            previous_answers=[],  # Start fresh
            chain_of_thought=False,
            use_llm=False,
            thresholds=STANDARD_THRESHOLDS,
            max_runtime_seconds=timeout_seconds
        )
    except Exception as e:
        # The timeout is now handled by checking if we ran out of time
        if timeout_seconds and (time.time() - start_time) >= timeout_seconds:
            timed_out = True
            error_message = f"Benchmark timed out after {timeout_seconds} seconds"
            print(f"  TIMEOUT after {timeout_seconds}s")
        else:
            error_message = str(e)
            print(f"  ERROR: {e}")
    
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
        'replication': replication,
        'total_runtime': total_runtime,
        'timed_out': timed_out,
        'error_message': error_message,
        'total_answers_generated': total_answers,
        'final_coherence_score': final_coherence,
        'final_dissimilarity_score': final_dissimilarity,
        'avg_coherence_score': avg_coherence,
        'answers_data': answers_generated[:5],  # Store first 5 answers for analysis
        'timestamp': datetime.now().isoformat()
    }
    
    status = "TIMEOUT" if timed_out else "COMPLETE" 
    print(f"  {status}: {total_runtime:.1f}s, {total_answers} answers, final_coherence={final_coherence}")
    
    return result

def run_proper_benchmark_timeout_experiment():
    """Run the proper benchmark timeout experiment"""
    
    print("PROPER BENCHMARK TIMEOUT EXPERIMENT")
    print("Testing full benchmark_question loops with timeouts")
    print("=" * 60)
    
    all_results = []
    
    # Test all scenarios
    test_scenarios = SLOW_SCENARIOS + [CONTROL_SCENARIO]
    
    total_tests = len(test_scenarios) * len(TIMEOUT_CONDITIONS) * 2  # 2 replications each
    current_test = 0
    
    for scenario in test_scenarios:
        for timeout_seconds, timeout_label in TIMEOUT_CONDITIONS:
            for replication in range(1, 3):  # 2 replications
                current_test += 1
                print(f"\n[{current_test}/{total_tests}] Testing scenario...")
                
                try:
                    result = run_benchmark_with_timeout(
                        scenario, timeout_seconds, timeout_label, replication
                    )
                    all_results.append(result)
                    
                    # Save intermediate results after each test
                    save_results(all_results, "proper_benchmark_timeout_results_intermediate.json")
                    
                except KeyboardInterrupt:
                    print("\nExperiment interrupted by user")
                    break
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    continue
    
    # Save final results
    save_results(all_results, "proper_benchmark_timeout_results_final.json")
    
    # Analyze results
    analyze_benchmark_timeout_results(all_results)
    
    return all_results

def save_results(results, filename):
    """Save results to JSON file"""
    output_data = {
        'metadata': {
            'experiment_type': 'proper_benchmark_timeout',
            'description': 'Testing full benchmark_question loops with timeouts',
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

def analyze_benchmark_timeout_results(results):
    """Analyze the benchmark timeout experiment results"""
    
    print("\n" + "="*60)
    print("BENCHMARK TIMEOUT EXPERIMENT ANALYSIS")
    print("="*60)
    
    # Group results by scenario and timeout
    from collections import defaultdict
    import statistics
    
    groups = defaultdict(lambda: defaultdict(list))
    
    for result in results:
        scenario_key = f"{result['model'].split('/')[-1]}_{result['question'][:30]}..."
        timeout_key = result['timeout_label']
        groups[scenario_key][timeout_key].append(result)
    
    print("\nRUNTIME ANALYSIS:")
    print("-" * 40)
    
    for scenario, timeout_groups in groups.items():
        print(f"\n{scenario}")
        for timeout_label in ['1hr', '2hr', 'unlimited']:
            if timeout_label in timeout_groups:
                results_group = timeout_groups[timeout_label]
                runtimes = [r['total_runtime'] for r in results_group]
                timeouts = [r['timed_out'] for r in results_group]
                
                if runtimes:
                    avg_runtime = statistics.mean(runtimes)
                    timeout_rate = sum(timeouts) / len(timeouts) * 100
                    print(f"  {timeout_label:10}: {avg_runtime:6.1f}s avg, {timeout_rate:4.0f}% timeout (n={len(runtimes)})")
    
    print("\nQUALITY ANALYSIS:")
    print("-" * 40)
    
    # Compare quality metrics between timeout conditions
    timeout_quality = defaultdict(list)
    timeout_answers = defaultdict(list)
    
    for result in results:
        if not result['timed_out'] and result['total_answers_generated'] > 0:
            timeout_quality[result['timeout_label']].append(result['avg_coherence_score'])
            timeout_answers[result['timeout_label']].append(result['total_answers_generated'])
    
    print("\nAverage quality by timeout condition:")
    for timeout_label in ['1hr', '2hr', 'unlimited']:
        if timeout_label in timeout_quality and timeout_quality[timeout_label]:
            quality_scores = timeout_quality[timeout_label]
            answer_counts = timeout_answers[timeout_label]
            
            avg_quality = statistics.mean(quality_scores)
            avg_answers = statistics.mean(answer_counts)
            
            print(f"  {timeout_label:10}: {avg_quality:5.1f} coherence, {avg_answers:5.1f} answers avg")
    
    # Recommendation
    print("\nRECOMMENDATION:")
    print("-" * 40)
    
    # Check if 1hr timeout significantly impacts quality
    if ('1hr' in timeout_quality and 'unlimited' in timeout_quality and 
        len(timeout_quality['1hr']) >= 3 and len(timeout_quality['unlimited']) >= 3):
        
        quality_1hr = statistics.mean(timeout_quality['1hr'])
        quality_unlimited = statistics.mean(timeout_quality['unlimited'])
        quality_diff = quality_1hr - quality_unlimited
        
        if abs(quality_diff) < 5:  # Less than 5 point difference
            print("✓ 1-hour timeout recommended: Minimal quality impact, prevents extreme delays")
        else:
            print(f"⚠ Quality difference detected: {quality_diff:+.1f} points (1hr vs unlimited)")
            print("Consider 2-hour timeout or investigate why quality drops with timeout")
    else:
        print("Need more data to make definitive recommendation")

if __name__ == "__main__":
    # Validate environment
    if not os.getenv("OPEN_ROUTER_KEY"):
        print("Error: OPEN_ROUTER_KEY environment variable not set")
        sys.exit(1)
        
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set") 
        sys.exit(1)
    
    print("WARNING: This experiment tests actual benchmark loops and may take several hours!")
    print("It will test timeout scenarios that historically took 5+ hours each.")
    print("Press Ctrl+C to interrupt at any time.\n")
    print("Starting experiment automatically...")
    
    run_proper_benchmark_timeout_experiment()