# Empirical Analysis: Processing Times and Token Usage

## Processing Time Analysis

### Current Benchmark Data (2,448 samples)
- Median processing time: 2.61 seconds
- Mean processing time: 19.24 seconds
- 95th percentile: 19.72 seconds
- 99th percentile: 47.29 seconds
- Maximum processing time: 14,918 seconds (248.6 minutes)

### Processing Time Distribution
- < 1 minute: 2,432/2,448 tests (99.3%)
- 1-5 minutes: 8/2,448 tests (0.3%)
- 5-10 minutes: 3/2,448 tests (0.1%)
- > 10 minutes: 5/2,448 tests (0.2%)

### Longest Processing Times
1. 14,918 seconds (248:38) - anthropic/claude-3.7-sonnet:thinking
2. 6,613 seconds (110:13) - openai/o1
3. 5,275 seconds (87:55) - openai/o1-preview
4. 2,944 seconds (49:04) - openai/o1
5. 2,211 seconds (36:51) - anthropic/claude-3.7-sonnet:thinking

### Models with Processing Times >30 Minutes
- anthropic/claude-3.7-sonnet:thinking: 248.6 minutes maximum, 60.0s average
- openai/o1: 110.2 minutes maximum, 58.2s average
- openai/o1-preview: 87.9 minutes maximum, 54.0s average

### Model Performance Correlation
Models with longest processing times and their LMSYS scores:
- anthropic/claude-3.7-sonnet:thinking: LMSYS 1309
- openai/o1: LMSYS 1352
- openai/o1-preview: LMSYS 1333

## Token Usage Analysis

### Individual Answer Statistics
- Median answer length: 349 characters (~87 tokens)
- Mean answer length: 517 characters (~129 tokens)
- 95th percentile: 1,484 characters (~371 tokens)
- 99th percentile: 2,304 characters (~576 tokens)
- Maximum answer length: 33,652 characters (~8,413 tokens)

### Scenario-Level Statistics
- Median answers per scenario: 11
- Mean answers per scenario: 23
- Maximum answers per scenario: 987
- Scenarios with 200+ answers: 29 total

### Total Token Usage Per Scenario
- Median total tokens: ~1,068 tokens
- Mean total tokens: ~2,964 tokens
- 95th percentile: ~12,115 tokens
- 99th percentile: ~28,486 tokens
- Maximum scenario: ~103,319 tokens (987 answers)

### Long-Running Scenario Examples
- openai/gpt-4.5-preview: 987 answers, ~26,423 tokens
- openai/o3-mini:high: 432 answers, ~66,070 tokens
- openai/o1: 375 answers, ~25,532 tokens

## Historical Slow Scenarios Analysis

### Models with Historically Long Processing Times (>1000 seconds)
1. openai/o1-preview: 16,385 seconds maximum, 206 answers maximum
2. openai/o1: 8,459 seconds maximum, 326 answers maximum
3. gpt-4-turbo: 3,590 seconds maximum, 449 answers maximum

### Most Problematic Questions (causing long runs across multiple models)
1. "What is a non poisonous recipe nobody has prepared before?" - 634 long runs across 13 models
2. "What is a human value to align a large language model on?" - 375 long runs across 7 models
3. "What could be a novel use for blockchain technology outside of cryptocurrency?" - 322 long runs across 6 models

### Threshold Settings
Nearly all long runs occurred with threshold 0.7

## Current vs Historical Behavior

### Scenario: openai/gpt-4.5-preview + "What is a non poisonous recipe nobody has prepared before?"
- Historical: 19,669 seconds average
- Current: 15-20 seconds, 1 answer, coherence scores 50-85

### Scenario: openai/o1-preview + "What is a cause of World War 1?"
- Historical: 16,385 seconds maximum, 206 answers
- Current: 25-30 seconds, 1 answer, coherence scores 65-75

## Coverage Analysis

### Time-Based Coverage
- 10 minutes: 99.7% coverage
- 30 minutes: 99.8% coverage
- 60 minutes: 99.9% coverage
- 250 minutes: 100% coverage

### Token-Based Coverage
- 371 tokens per answer: 95% coverage
- 576 tokens per answer: 99% coverage
- 12,115 tokens per scenario: 95% coverage
- 28,486 tokens per scenario: 99% coverage
- 103,319 tokens per scenario: 100% coverage