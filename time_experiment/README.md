# Time and Token Limit Analysis

Empirical analysis of processing times and token usage patterns for implementing practical timeout and token limits in AidanBench.

## Key Files
- `empirical_analysis.md` - Complete analysis of processing times and token usage
- `proper_benchmark_timeout_test.py` - Full benchmark loop timeout testing
- `focused_timeout_test.py` - Tests using historically slow model/question combinations
- `realistic_timeout_experiment.py` - Original timeout experiment (single API calls)
- `benchmark_with_timeout.py` - Timeout-enabled benchmark function for testing

## Results Summary
- 99.3% of benchmark tests complete in under 1 minute
- 99.8% complete in under 30 minutes
- Top reasoning models (o1, o1-preview, claude-3.7-sonnet:thinking) can take 30+ minutes on complex questions
- Token usage ranges from ~1,000 tokens (typical) to 100,000+ tokens (extreme cases)
- Historical "slow" scenarios now complete quickly due to model improvements