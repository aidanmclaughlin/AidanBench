# Aidan Bench
Some models feel competent despite under-scoring on benchmarks like MMLU, GPQA, MATH, or NIAH.

*Aidan Bench* rewards:

1. Creativity
2. Reliability
3. Contextual attention
4. Instruction following

**Aidan Bench is weakly correlated with Lmsys, has no score ceiling, and aligns with real-world open-ended use.**

# Methodology

We give LLMs a set of open-ended questions spanning various domains:

```python
"Provide an explanation for Japan's Lost Decades.",
"How might you use a brick and a blanket?",
"What architectural features might you include in a tasteful house?",
"Propose a solution to Los Angeles traffic.",
"What activities might I include at a party for firefighters?",
"How could we redesign schools to better prepare students for the 22nd century?",
# ... and many more
```

For each question, we ask the model to generate novel answers while avoiding previous responses. The benchmark continues generating answers until either:

1. The answer becomes incoherent (coherence score ≤ 15/100)
2. The answer is too similar to previous responses (embedding similarity ≥ 0.85)

## Scoring System

For each question q and model M, we compute the score S_M(q) as the maximum number of valid responses that satisfy both coherence and novelty thresholds:

1. **Coherence Score (C)**: Each response is evaluated by a judge model (o1-mini) on a scale of 0-100. Responses must maintain C > 15 to be considered valid.

2. **Novelty Score (N)**: For each new response r, we compute:
   ```
   N = 1 - max(cosine_similarity(e_new, e_prev))
   ```
   where e_new is the embedding of the new response and e_prev are embeddings of all previous responses. Responses must maintain N > 0.15 to be considered valid.

The final score for a model is the sum of valid responses across all questions before either threshold is breached. This straightforward scoring mechanism offers:

- Clear interpretability ("Model X generated Y unique answers")
- Robustness through simple failure detection
- Reliability through objective thresholds

# Results

Here are the latest benchmark results across various models:

![Benchmark results across models](results.png)

We test models at temperature=0.7.

# Setup

## Prerequisites

- Python 3.x
- OpenAI API key
- OpenRouter API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/aidanmclaughlin/Aidan-Bench.git
   cd Aidan-Bench
   ```

2. Install required packages:
   ```bash
   pip install numpy openai colorama retry
   ```

3. Set up environment variables:
   ```bash
   export OPENAI_API_KEY="your-openai-key"
   export OPEN_ROUTER_KEY="your-openrouter-key"
   ```

## Running the Benchmark

Run the benchmark with:
```bash
python main.py
```

The script will guide you through several choices:

1. Select model(s) to benchmark
   - Choose from a list of supported models
   - Option to test multiple models in sequence

2. Configure test parameters
   - Threading mode (multi-threaded or single-threaded)
   - Temperature setting (default: 0.7)
   - Number of questions to test
   - Use of LLM judge for similarity scoring

3. Set thresholds (optional)
   - Coherence score threshold
   - Embedding similarity threshold
   - LLM similarity threshold (if using LLM judge)

Results will be saved to `results.json` and can be visualized using the included visualization tool.

## Visualization

After running the benchmark, you can visualize results using the included visualization tool:

```bash
cd visualize_results
python -m http.server 8000
```

Then open `http://localhost:8000/visualization` in your browser to explore the results interactively.

