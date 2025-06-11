#!/usr/bin/env python3
"""
Token Usage Summary for AidanBench
Provides clear recommendations for token limits based on comprehensive analysis.
"""

# Analysis results from the comprehensive dataset (results.json with 80,788 answers)
ANALYSIS_DATA = {
    "total_answers": 80788,
    "total_scenarios": 3524,
    "answer_stats": {
        "avg_length_chars": 517,
        "median_length_chars": 349,
        "max_length_chars": 33652,
        "avg_tokens": 129,
        "median_tokens": 87,
        "max_tokens": 8413,
        "percentiles": {
            "p50": 87,
            "p90": 270,
            "p95": 371,
            "p99": 576,
            "p100": 8413
        }
    },
    "scenario_stats": {
        "avg_answers_per_scenario": 22.9,
        "median_answers_per_scenario": 11,
        "max_answers_per_scenario": 987,
        "avg_total_tokens": 2964,
        "median_total_tokens": 1068,
        "max_total_tokens": 103319,
        "percentiles": {
            "p50": 1068,
            "p90": 7218,
            "p95": 12115,
            "p99": 28486,
            "p100": 103319
        }
    },
    "long_scenarios": [
        ("gpt-4.5-preview", "What is a non poisonous recipe nobody has prepared before?", 987, 26423),
        ("o3-mini:high", "Propose an alternative to democracy for successfully and fairly governing a large nation.", 432, 66070),
        ("o1", "Imagine a competition where contestants build habitats for animals; what competitions would be most interesting?", 375, 25532),
        ("o3-mini:high", "What is a non poisonous recipe nobody has prepared before?", 369, 85020),
        ("o1", "What is a non poisonous recipe nobody has prepared before?", 352, 55809),
        ("o1", "What activities might I include at a party for firefighters?", 351, 16065),
        ("o3-mini:medium", "Propose an alternative to democracy for successfully and fairly governing a large nation.", 342, 44620),
        ("o1", "What could be a novel use for blockchain technology outside of cryptocurrency?", 326, 16403),
        ("o3-mini:high", "Describe a new form of professional sports that focuses on non-competitive collaboration.", 320, 62604),
        ("o3-mini:high", "What activities might I include at a party for firefighters?", 313, 19836)
    ]
}

def print_summary():
    """Print comprehensive token usage summary and recommendations"""
    print("=" * 80)
    print("AIDANBENCH TOKEN USAGE ANALYSIS SUMMARY")
    print("=" * 80)
    
    print(f"\nDATASET OVERVIEW:")
    print(f"• Total answers analyzed: {ANALYSIS_DATA['total_answers']:,}")
    print(f"• Total scenarios analyzed: {ANALYSIS_DATA['total_scenarios']:,}")
    print(f"• Average answers per scenario: {ANALYSIS_DATA['scenario_stats']['avg_answers_per_scenario']:.1f}")
    print(f"• Median answers per scenario: {ANALYSIS_DATA['scenario_stats']['median_answers_per_scenario']}")
    print(f"• Maximum answers in single scenario: {ANALYSIS_DATA['scenario_stats']['max_answers_per_scenario']:,}")
    
    print(f"\nANSWER LENGTH PATTERNS:")
    a = ANALYSIS_DATA['answer_stats']
    print(f"• Typical answer length: {a['median_length_chars']} characters (~{a['median_tokens']} tokens)")
    print(f"• Average answer length: {a['avg_length_chars']} characters (~{a['avg_tokens']} tokens)")
    print(f"• Longest single answer: {a['max_length_chars']:,} characters (~{a['max_tokens']:,} tokens)")
    
    print(f"\nANSWER TOKEN DISTRIBUTION:")
    p = a['percentiles']
    print(f"• 50% of answers use ≤ {p['p50']} tokens")
    print(f"• 90% of answers use ≤ {p['p90']} tokens")
    print(f"• 95% of answers use ≤ {p['p95']} tokens")
    print(f"• 99% of answers use ≤ {p['p99']} tokens")
    print(f"• 100% of answers use ≤ {p['p100']:,} tokens")
    
    print(f"\nSCENARIO-LEVEL TOKEN USAGE:")
    s = ANALYSIS_DATA['scenario_stats']
    print(f"• Typical scenario total: ~{s['median_total_tokens']:,} tokens")
    print(f"• Average scenario total: ~{s['avg_total_tokens']:,} tokens")
    print(f"• Largest scenario total: {s['max_total_tokens']:,} tokens")
    
    print(f"\nSCENARIO TOKEN DISTRIBUTION:")
    sp = s['percentiles']
    print(f"• 50% of scenarios use ≤ {sp['p50']:,} tokens total")
    print(f"• 90% of scenarios use ≤ {sp['p90']:,} tokens total")
    print(f"• 95% of scenarios use ≤ {sp['p95']:,} tokens total")
    print(f"• 99% of scenarios use ≤ {sp['p99']:,} tokens total")
    print(f"• 100% of scenarios use ≤ {sp['p100']:,} tokens total")
    
    print(f"\nEXTREME SCENARIOS (200+ answers):")
    print(f"Found {len(ANALYSIS_DATA['long_scenarios'])} scenarios with 200+ answers:")
    for i, (model, question, answers, tokens) in enumerate(ANALYSIS_DATA['long_scenarios'][:5], 1):
        short_question = question[:60] + "..." if len(question) > 60 else question
        print(f"  {i}. {model}: '{short_question}'")
        print(f"     {answers:,} answers, {tokens:,} tokens total")
    
    print(f"\n" + "=" * 80)
    print("TOKEN LIMIT RECOMMENDATIONS")
    print("=" * 80)
    
    print(f"\nPER-ANSWER TOKEN LIMITS:")
    print(f"• Conservative (95% coverage): {p['p95']} tokens")
    print(f"• Comprehensive (99% coverage): {p['p99']} tokens")
    print(f"• Maximum (100% coverage): {p['p100']:,} tokens")
    print(f"  - Note: 100% coverage requires very high limits due to outliers")
    print(f"  - Consider timeouts/truncation instead of accommodating all outliers")
    
    print(f"\nPER-SCENARIO TOKEN LIMITS (total for all answers in scenario):")
    print(f"• Conservative (95% coverage): {sp['p95']:,} tokens")
    print(f"• Comprehensive (99% coverage): {sp['p99']:,} tokens")
    print(f"• Maximum (100% coverage): {sp['p100']:,} tokens")
    
    print(f"\nPRACTICAL RECOMMENDATIONS:")
    print(f"• For typical usage: Set per-answer limit to {p['p95']} tokens")
    print(f"• For comprehensive testing: Set per-scenario limit to {sp['p95']:,} tokens")
    print(f"• For extreme scenarios: Consider {sp['p99']:,} tokens per scenario")
    print(f"• Use timeouts to prevent runaway generation (some scenarios hit 200+ answers)")
    print(f"• Monitor token usage patterns in your specific use case")
    
    print(f"\nTRADE-OFFS:")
    print(f"• 95% limits miss ~{ANALYSIS_DATA['total_answers'] * 0.05:,.0f} answers but are practical")
    print(f"• 99% limits miss ~{ANALYSIS_DATA['total_answers'] * 0.01:,.0f} answers but are generous")
    print(f"• 100% limits accommodate all cases but may be prohibitively expensive")
    
    print(f"\nCOST ESTIMATES (approximate, varies by model):")
    # Rough estimates assuming $0.01 per 1K tokens (varies widely by model)
    cost_per_1k = 0.01
    print(f"• Conservative scenario (~{sp['p95']:,} tokens): ${sp['p95'] * cost_per_1k / 1000:.2f}")
    print(f"• Comprehensive scenario (~{sp['p99']:,} tokens): ${sp['p99'] * cost_per_1k / 1000:.2f}")
    print(f"• Extreme scenario (~{sp['p100']:,} tokens): ${sp['p100'] * cost_per_1k / 1000:.2f}")
    print(f"• Note: Actual costs vary significantly by model and provider")

if __name__ == "__main__":
    print_summary()