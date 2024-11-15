from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import product
from typing import Optional
from benchmark import benchmark_question
from model_list import models
from question_list import questions
import argparse
import sys


def benchmark_model(
    model_names: list[str],
    multithreaded: bool = True,
    temperatures: list[float] = [0.7],
    chain_of_thought: bool = False,
    use_llm: bool = False,
    num_runs: int = 1,
    num_questions: Optional[int] = None
):
    questions_to_use = questions[:num_questions] if num_questions else questions

    try:
        if multithreaded:
            with ThreadPoolExecutor(max_workers=200) as executor:
                future_to_params = {
                    executor.submit(
                        benchmark_question,
                        question,
                        model_name,
                        temperature,
                        chain_of_thought,
                        use_llm
                    ): (question, model_name, temperature)
                    for model_name, temperature in product(model_names, temperatures)
                    for _ in range(num_runs)
                    for question in questions_to_use
                }

                # Process futures as they complete
                for future in as_completed(future_to_params):
                    question, model_name, temperature = future_to_params[future]
                    try:
                        future.result()
                    except Exception as e:
                        print(
                            f"{Fore.RED}Error for model '{model_name}', temperature {temperature}, question '{question}': {e}{Style.RESET_ALL}"
                        )
        else:
            for model_name, temperature in product(model_names, temperatures):
                for _ in range(num_runs):
                    for question in questions_to_use:
                        try:
                            benchmark_question(
                                question,
                                model_name,
                                temperature,
                                chain_of_thought,
                                use_llm
                            )
                        except Exception as e:
                            print(
                                f"{Fore.RED}Error for model '{model_name}', temperature {temperature}, question '{question}': {e}{Style.RESET_ALL}"
                            )
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Benchmark interrupted by user. Exiting...{Style.RESET_ALL}")
        sys.exit(0)


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Benchmark a language model.")
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "--model-name",
            type=str,
            help="Name of the model to benchmark"
        )
        group.add_argument(
            "--all-models",
            action="store_true",
            help="Benchmark all available models"
        )
        parser.add_argument(
            "--temp-range",
            action="store_true",
            help="Benchmark with temperatures from 0 to 1 in 0.1 increments"
        )
        parser.add_argument(
            "--single-threaded",
            action="store_true",
            help="Run in single-threaded mode"
        )
        parser.add_argument(
            "--temperature",
            type=float,
            default=0.7,
            help="Temperature for generation"
        )
        parser.add_argument(
            "--chain-of-thought",
            action="store_true",
            help="Enable chain-of-thought prompting"
        )
        parser.add_argument(
            "--use-llm-similarity",
            action="store_true",
            help="Use LLM to judge answer similarity instead of embeddings"
        )
        parser.add_argument(
            "--num-runs",
            type=int,
            default=1,
            help="Number of identical runs to perform"
        )
        parser.add_argument(
            "--num-questions",
            type=int,
            default=None,
            help="Number of questions to benchmark. Use all if not specified."
        )
        args = parser.parse_args()

        if args.all_models:
            model_names = models
        else:
            model_names = [args.model_name]

        benchmark_model(
            model_names,
            not args.single_threaded,
            [round(t * 0.1, 1) for t in range(11)] if args.temp_range else [args.temperature],
            args.chain_of_thought,
            args.use_llm_similarity,
            args.num_runs,
            args.num_questions
        )
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Benchmark interrupted by user. Exiting...{Style.RESET_ALL}")
        sys.exit(0)
