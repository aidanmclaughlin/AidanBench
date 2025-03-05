import json
from colorama import Fore, Style
from benchmark.model_list import models


def load_results(file_path='results.json'):
    with open(file_path, 'r') as f:
        return json.load(f)


def visualize_progress(results, thresholds):
    total_questions = 0
    completed_questions = 0
    incomplete_pairs = []

    print(f"{Fore.YELLOW}Benchmark Progress Visualization{Style.RESET_ALL}")
    print("=" * 50)

    for model in models:
        temps = results['models'].get(model, {})
        if not temps:
            print(f"Model: {Fore.CYAN}{model}{Style.RESET_ALL} | No progress yet")
            print(f"Completion: [{Fore.RED}{'-' * 50}{Style.RESET_ALL}] 0.00% (0/0)")
            print("-" * 50)
            continue

        for temp, questions in temps.items():
            model_total = len(questions)
            model_completed = 0

            for question, answers in questions.items():
                last_answer = answers[-1]
                if (last_answer['coherence_score'] <= thresholds['coherence_score'] or
                    last_answer['embedding_dissimilarity_score'] <= thresholds['embedding_dissimilarity_score'] or
                    ('llm_dissimilarity_score' in last_answer and
                     last_answer['llm_dissimilarity_score'] <= thresholds['llm_dissimilarity_score'])):
                    model_completed += 1
                else:
                    incomplete_pairs.append((model, temp, question))

            total_questions += model_total
            completed_questions += model_completed

            completion_percentage = (model_completed / model_total) * 100 if model_total else 0
            bar_length = int(completion_percentage // 2)
            bar = f"[{Fore.GREEN}{'#' * bar_length}{Fore.RED}{'-' * (50 - bar_length)}{Style.RESET_ALL}]"

            print(f"Model: {Fore.CYAN}{model}{Style.RESET_ALL} | Temp: {temp}")
            print(f"Completion: {bar} {completion_percentage:.2f}% ({model_completed}/{model_total})")
            print("-" * 50)

    overall_completion = (completed_questions / total_questions) * 100 if total_questions else 0
    print(f"{Fore.MAGENTA}Overall Benchmark Completion: {overall_completion:.2f}% ({completed_questions}/{total_questions}){Style.RESET_ALL}")

    if incomplete_pairs:
        print(f"\n{Fore.YELLOW}Incomplete Question/Model Pairs:{Style.RESET_ALL}")
        for model, temp, question in incomplete_pairs:
            print(f"- Model: {model}, Temp: {temp}, Question: {question}")
    else:
        print(f"{Fore.GREEN}All benchmarks completed!{Style.RESET_ALL}")


if __name__ == "__main__":
    thresholds = {
        'coherence_score': 15,
        'embedding_dissimilarity_score': 0.15,
        'llm_dissimilarity_score': 0.15
    }

    results = load_results()
    visualize_progress(results, thresholds)
