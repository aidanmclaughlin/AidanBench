#!/usr/bin/env python3
"""
Quick test version to verify the timeout experiment works
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

# Quick test scenario
QUICK_SCENARIO = {
    "model": "openai/gpt-4o-mini-2024-07-18",
    "question": "What color is the sky?",
    "description": "Quick test scenario"
}

STANDARD_THRESHOLDS = {
    'coherence_score': 15,
    'embedding_dissimilarity_score': 0.1,
    'llm_dissimilarity_score': 0.1
}

def run_quick_test():
    print("QUICK TIMEOUT TEST")
    print("Testing with a simple scenario and 30-second timeout")
    print("=" * 50)
    
    start_time = time.time()
    
    try:
        print(f"Testing: {QUICK_SCENARIO['model']}")
        print(f"Question: {QUICK_SCENARIO['question']}")
        print("Running with 30-second timeout...\n")
        
        answers = benchmark_question_with_timeout(
            question=QUICK_SCENARIO['question'],
            model_name=QUICK_SCENARIO['model'],
            temperature=0.7,
            previous_answers=[],
            chain_of_thought=False,
            use_llm=False,
            thresholds=STANDARD_THRESHOLDS,
            max_runtime_seconds=30  # 30-second timeout
        )
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"\n✓ Test completed successfully!")
        print(f"Total runtime: {total_time:.1f} seconds")
        print(f"Answers generated: {len(answers)}")
        
        if answers:
            print(f"First answer: {answers[0]['answer'][:100]}...")
            print(f"Final coherence: {answers[-1]['coherence_score']}")
        
        # Save result
        result = {
            'test_type': 'quick_timeout_test',
            'scenario': QUICK_SCENARIO,
            'timeout_seconds': 30,
            'total_runtime': total_time,
            'answers_generated': len(answers),
            'answers': answers,
            'timestamp': datetime.now().isoformat()
        }
        
        with open('quick_timeout_test_result.json', 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"\nResult saved to quick_timeout_test_result.json")
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = run_quick_test()
    if success:
        print("\n✓ Quick test passed! The full timeout experiment should work.")
    else:
        print("\n✗ Quick test failed. Check the setup before running full experiment.")