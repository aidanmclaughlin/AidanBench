#!/usr/bin/env python3
"""
Quick test to verify basic functionality before running the full experiment
"""

import os
import sys

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
except ImportError:
    print("python-dotenv not available, using system environment variables")

# Add paths
parent_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(parent_dir)
sys.path.append(os.path.join(parent_dir, 'benchmark'))

print("Testing basic imports...")
try:
    # Change to parent directory and import
    os.chdir(parent_dir)
    from benchmark.benchmark import benchmark_question
    print("✓ benchmark_question imported successfully")
except Exception as e:
    print(f"✗ Error importing benchmark_question: {e}")
    sys.exit(1)

print("\nTesting environment variables...")
required_vars = ['OPEN_ROUTER_KEY', 'OPENAI_API_KEY']
for var in required_vars:
    if os.getenv(var):
        print(f"✓ {var} is set")
    else:
        print(f"✗ {var} is missing")
        sys.exit(1)

print("\nTesting basic benchmark_question call...")
STANDARD_THRESHOLDS = {
    'coherence_score': 15,
    'embedding_dissimilarity_score': 0.1,
    'llm_dissimilarity_score': 0.1
}

try:
    # Test a very simple scenario with short timeout
    result = benchmark_question(
        question="What color is the sky?",
        model_name="openai/gpt-4o-mini-2024-07-18",
        temperature=0.7,
        previous_answers=[],
        chain_of_thought=False,
        use_llm=False,
        thresholds=STANDARD_THRESHOLDS,
        max_runtime_seconds=30  # 30 second timeout
    )
    
    print(f"✓ Basic test successful! Generated {len(result)} answers")
    if result:
        print(f"  First answer: {result[0]['answer'][:50]}...")
        print(f"  Processing time: {result[0]['processing_time']:.1f}s")
    
except Exception as e:
    print(f"✗ Basic test failed: {e}")
    sys.exit(1)

print("\n✓ All basic functionality tests passed!")
print("The proper benchmark timeout test should work correctly.")