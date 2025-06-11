#!/usr/bin/env python3
"""
Analyze token usage patterns in benchmark results to determine appropriate limits.
"""

import json
import statistics
from collections import defaultdict
import os

def estimate_tokens(text):
    """Estimate tokens using ~4 characters per token rule"""
    if not text:
        return 0
    return len(text) / 4

def analyze_results_file(filepath):
    """Analyze a single results file for token usage patterns"""
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return None
    
    print(f"\nAnalyzing: {filepath}")
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None
    
    answer_lengths = []
    answer_counts = defaultdict(int)
    processing_times = []
    token_estimates = []
    scenario_data = []
    
    # Handle different file formats
    if 'results' in data:
        results = data['results']
    elif isinstance(data, list):
        results = data
    elif 'models' in data:
        # Handle the models format from cot.json and similar files
        results = []
        for model, temp_data in data['models'].items():
            for temp, questions in temp_data.items():
                for question, answers in questions.items():
                    for answer_data in answers:
                        # Convert to uniform format
                        result = {
                            'model': model,
                            'temperature': temp,
                            'question': question,
                            'answer': answer_data.get('answer', ''),
                            'answer_num': answer_data.get('answer_num', 1),
                            'answer_length': len(answer_data.get('answer', '')),
                            'processing_time': answer_data.get('processing_time', 0),
                            'coherence_score': answer_data.get('coherence_score', 0)
                        }
                        results.append(result)
    else:
        # Try to find results in nested structure
        results = []
        for key, value in data.items():
            if isinstance(value, list):
                results.extend(value)
    
    if not results:
        print("No results found in expected format")
        return None
    
    print(f"Found {len(results)} results")
    
    # Group by scenario/question to count answers per scenario
    scenario_answers = defaultdict(list)
    
    for result in results:
        # Extract answer text and length
        answer_text = ""
        answer_len = 0
        
        if 'answer' in result:
            answer_text = result['answer']
            answer_len = len(answer_text) if answer_text else 0
        elif 'response' in result:
            answer_text = result['response']
            answer_len = len(answer_text) if answer_text else 0
        elif 'answer_length' in result:
            answer_len = result['answer_length']
        
        if answer_len > 0:
            answer_lengths.append(answer_len)
            token_estimates.append(estimate_tokens(answer_text or "x" * answer_len))
        
        # Track processing time
        if 'processing_time' in result:
            processing_times.append(result['processing_time'])
        
        # Group by scenario
        scenario_key = f"{result.get('model', 'unknown')}_{result.get('question', 'unknown')}"
        scenario_answers[scenario_key].append({
            'length': answer_len,
            'tokens': estimate_tokens(answer_text or "x" * answer_len),
            'answer_num': result.get('answer_num', 1),
            'timeout': result.get('timed_out', False)
        })
    
    if not answer_lengths:
        print("No answer length data found")
        return None
    
    # Calculate statistics
    stats = {
        'total_answers': len(answer_lengths),
        'total_scenarios': len(scenario_answers),
        'avg_answer_length': statistics.mean(answer_lengths),
        'median_answer_length': statistics.median(answer_lengths),
        'min_answer_length': min(answer_lengths),
        'max_answer_length': max(answer_lengths),
        'avg_tokens_per_answer': statistics.mean(token_estimates),
        'median_tokens_per_answer': statistics.median(token_estimates),
        'percentiles': {
            'p50_length': statistics.quantiles(answer_lengths, n=100)[49],
            'p90_length': statistics.quantiles(answer_lengths, n=100)[89],
            'p95_length': statistics.quantiles(answer_lengths, n=100)[94],
            'p99_length': statistics.quantiles(answer_lengths, n=100)[98],
            'p50_tokens': statistics.quantiles(token_estimates, n=100)[49],
            'p90_tokens': statistics.quantiles(token_estimates, n=100)[89],
            'p95_tokens': statistics.quantiles(token_estimates, n=100)[94],
            'p99_tokens': statistics.quantiles(token_estimates, n=100)[98],
        }
    }
    
    # Analyze scenarios (how many answers per scenario)
    answers_per_scenario = []
    total_tokens_per_scenario = []
    
    for scenario, answers in scenario_answers.items():
        num_answers = len(answers)
        total_scenario_tokens = sum(a['tokens'] for a in answers)
        answers_per_scenario.append(num_answers)
        total_tokens_per_scenario.append(total_scenario_tokens)
    
    if answers_per_scenario:
        stats['scenarios'] = {
            'avg_answers_per_scenario': statistics.mean(answers_per_scenario),
            'median_answers_per_scenario': statistics.median(answers_per_scenario),
            'max_answers_per_scenario': max(answers_per_scenario),
            'min_answers_per_scenario': min(answers_per_scenario),
            'avg_total_tokens_per_scenario': statistics.mean(total_tokens_per_scenario),
            'median_total_tokens_per_scenario': statistics.median(total_tokens_per_scenario),
            'max_total_tokens_per_scenario': max(total_tokens_per_scenario),
            'scenario_token_percentiles': {
                'p50': statistics.quantiles(total_tokens_per_scenario, n=100)[49],
                'p90': statistics.quantiles(total_tokens_per_scenario, n=100)[89],
                'p95': statistics.quantiles(total_tokens_per_scenario, n=100)[94],
                'p99': statistics.quantiles(total_tokens_per_scenario, n=100)[98],
            } if len(total_tokens_per_scenario) >= 100 else {}
        }
    
    # Find long-running scenarios (200+ answers mentioned in prompt)
    long_scenarios = [(k, len(v)) for k, v in scenario_answers.items() if len(v) >= 200]
    if long_scenarios:
        print(f"\nFound {len(long_scenarios)} scenarios with 200+ answers:")
        for scenario, count in sorted(long_scenarios, key=lambda x: x[1], reverse=True)[:10]:
            total_tokens = sum(a['tokens'] for a in scenario_answers[scenario])
            print(f"  {scenario[:80]}... : {count} answers, ~{total_tokens:.0f} tokens")
    
    return stats

def main():
    """Main analysis function"""
    print("=== BENCHMARK TOKEN USAGE ANALYSIS ===")
    
    # List of result files to analyze
    result_files = [
        "/Users/anuja/AidanBench/time_experiment/comprehensive_final_results.json",
        "/Users/anuja/AidanBench/time_experiment/realistic_timeout_results_final.json",
        "/Users/anuja/AidanBench/results/results.json",
        "/Users/anuja/AidanBench/results.json",
        "/Users/anuja/AidanBench/results/cot.json",  # This has the 200+ answer scenarios
        "/Users/anuja/AidanBench/results/not_cot.json"
    ]
    
    all_stats = {}
    
    for filepath in result_files:
        stats = analyze_results_file(filepath)
        if stats:
            filename = os.path.basename(filepath)
            all_stats[filename] = stats
            
            print(f"\n--- RESULTS FOR {filename} ---")
            print(f"Total answers: {stats['total_answers']:,}")
            print(f"Total scenarios: {stats['total_scenarios']:,}")
            print(f"Average answer length: {stats['avg_answer_length']:.0f} characters")
            print(f"Median answer length: {stats['median_answer_length']:.0f} characters")
            print(f"Max answer length: {stats['max_answer_length']:,} characters")
            print(f"Average tokens per answer: {stats['avg_tokens_per_answer']:.0f}")
            print(f"Median tokens per answer: {stats['median_tokens_per_answer']:.0f}")
            
            print(f"\nPERCENTILE ANALYSIS:")
            print(f"  50th percentile: {stats['percentiles']['p50_length']:.0f} chars (~{stats['percentiles']['p50_tokens']:.0f} tokens)")
            print(f"  90th percentile: {stats['percentiles']['p90_length']:.0f} chars (~{stats['percentiles']['p90_tokens']:.0f} tokens)")
            print(f"  95th percentile: {stats['percentiles']['p95_length']:.0f} chars (~{stats['percentiles']['p95_tokens']:.0f} tokens)")
            print(f"  99th percentile: {stats['percentiles']['p99_length']:.0f} chars (~{stats['percentiles']['p99_tokens']:.0f} tokens)")
            
            if 'scenarios' in stats:
                s = stats['scenarios']
                print(f"\nSCENARIO ANALYSIS:")
                print(f"  Average answers per scenario: {s['avg_answers_per_scenario']:.1f}")
                print(f"  Median answers per scenario: {s['median_answers_per_scenario']:.0f}")
                print(f"  Max answers per scenario: {s['max_answers_per_scenario']:,}")
                print(f"  Average total tokens per scenario: {s['avg_total_tokens_per_scenario']:.0f}")
                print(f"  Median total tokens per scenario: {s['median_total_tokens_per_scenario']:.0f}")
                print(f"  Max total tokens per scenario: {s['max_total_tokens_per_scenario']:,}")
                
                if s['scenario_token_percentiles']:
                    print(f"  Scenario token percentiles:")
                    print(f"    50th percentile: {s['scenario_token_percentiles']['p50']:.0f} tokens")
                    print(f"    90th percentile: {s['scenario_token_percentiles']['p90']:.0f} tokens")
                    print(f"    95th percentile: {s['scenario_token_percentiles']['p95']:.0f} tokens")
                    print(f"    99th percentile: {s['scenario_token_percentiles']['p99']:.0f} tokens")
    
    # Calculate recommended token limits
    print(f"\n=== RECOMMENDED TOKEN LIMITS ===")
    
    # Find the most comprehensive dataset
    best_stats = None
    best_count = 0
    for filename, stats in all_stats.items():
        if stats['total_answers'] > best_count:
            best_count = stats['total_answers']
            best_stats = stats
    
    if best_stats and 'scenarios' in best_stats:
        s = best_stats['scenarios']
        print(f"Based on {best_count:,} answers from the most comprehensive dataset:")
        print(f"\nPER-ANSWER TOKEN LIMITS:")
        print(f"  For 95% of answers: {best_stats['percentiles']['p95_tokens']:.0f} tokens")
        print(f"  For 99% of answers: {best_stats['percentiles']['p99_tokens']:.0f} tokens")
        print(f"  For 100% of answers: {estimate_tokens('x' * best_stats['max_answer_length']):.0f} tokens")
        
        if s['scenario_token_percentiles']:
            print(f"\nPER-SCENARIO TOKEN LIMITS (total for all answers in scenario):")
            print(f"  For 95% of scenarios: {s['scenario_token_percentiles']['p95']:.0f} tokens")
            print(f"  For 99% of scenarios: {s['scenario_token_percentiles']['p99']:.0f} tokens")
            print(f"  For 100% of scenarios: {s['max_total_tokens_per_scenario']:.0f} tokens")
    
    print(f"\n=== SUMMARY INSIGHTS ===")
    if best_stats:
        print(f"- Most answers are relatively short (~{best_stats['median_tokens_per_answer']:.0f} tokens)")
        if 'scenarios' in best_stats:
            s = best_stats['scenarios']
            print(f"- Scenarios typically generate {s['median_answers_per_scenario']:.0f} answers")
            print(f"- Some scenarios can generate up to {s['max_answers_per_scenario']:,} answers")
            print(f"- Long scenarios can use up to {s['max_total_tokens_per_scenario']:,} tokens total")
        print(f"- Token limits should account for both individual answer length and scenario totals")

if __name__ == "__main__":
    main()