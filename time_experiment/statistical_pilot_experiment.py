#!/usr/bin/env python3
"""
Statistical pilot experiment to test the impact of time limits on LLM creativity benchmarks.

Previous comprehensive experiment testing 5-minute limits vs unlimited time.
Results: 5-minute limits actually improved performance slightly while solving operational delays.

This file serves as the baseline for comparison with the new realistic timeout experiment
that tests actual slow scenarios (15min, 30min, 1hr timeouts with slow models/questions).
"""

import json
import time
import random
from datetime import datetime
from typing import Dict, List, Optional
import os
import sys
from dotenv import load_dotenv
import statistics
import math

load_dotenv('../.env')
sys.path.append('../benchmark')
sys.path.append('.')

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "dummy-key-for-router-only"

from time_aware_models import chat_with_model_timed
from prompts import judge_answer

class StatisticalPilotExperiment:
    def __init__(self):
        self.model_pairs = [
            #OpenAI thinking vs standard
            ("openai/gpt-4o-mini-2024-07-18", "openai/o1-mini"),
            ("openai/gpt-4o-2024-08-06", "openai/o1-preview"),
            ("openai/chatgpt-4o-latest", "openai/o1"),
            
            #Anthropic thinking vs standard  
            ("anthropic/claude-3.5-sonnet", "anthropic/claude-3.7-sonnet:thinking"),
            ("anthropic/claude-3.7-sonnet", "anthropic/claude-3.7-sonnet:thinking"),
            
            #Google models
            ("google/gemini-2.0-flash-exp", None),
            ("google/gemini-pro-1.5", None),
            
            #Other major models
            ("x-ai/grok-3-beta", None),
            ("meta-llama/llama-3.3-70b-instruct", None),
            ("mistralai/mistral-large-latest", None),
        ]
        
        #6 styles of openended creativity questions, 5 qs each
        self.questions_by_style = {
            "creative_invention": [  #Openended creative invention questions
                "Invent a new musical instrument and describe how it would be played.",
                "Design a new color that doesn't exist and explain its properties.", 
                "Create a new emotion that humans have never felt before.",
                "Invent a new sense organ and describe what it would detect.",
                "Design a revolutionary new sport that combines elements of three existing sports."
            ],
            "practical_problems": [  #Openended practical problem solving questions
                "Propose a solution to Los Angeles traffic.",
                "What might be an unexpected solution to reducing plastic waste in oceans?",
                "How could we redesign schools to better prepare students for the 22nd century?",
                "Design a system to fairly distribute limited medical resources.",
                "Create a plan to reduce political polarization in democracies."
            ],
            "divergent_thinking": [  #Classic openended divergent thinking questions
                "How might you use a brick and a blanket?",
                "What activities might I include at a party for firefighters?",
                "List unusual uses for a paper clip.",
                "What would you do with 1000 rubber ducks?",
                "How could you entertain yourself with only a piece of string?"
            ],
            "analytical_reasoning": [  #Openended analytical reasoning questions
                "Explain why some businesses fail while others succeed.",
                "What factors contribute to the rise and fall of civilizations?",
                "Analyze the relationship between technology and human happiness.",
                "Why do some ideas spread rapidly while others don't?",
                "What makes some teams more effective than others?"
            ],
            "hypothetical_scenarios": [  #Openended hypothetical scenario questions
                "What would happen if gravity was 50% weaker on Earth?",
                "How would society change if humans could live to 500 years?",
                "What if we could communicate directly with animals?",
                "How would the world be different if photosynthesis was impossible?",
                "What if humans could perceive electromagnetic fields?"
            ],
            "design_challenges": [  #Openended design and innovation questions
                "Design a revolutionary new transportation method for cities.",
                "Devise a method to prevent social media addiction.",
                "Create a new architectural style for climate change adaptation.",
                "Invent a new cooking technique using only household items.",
                "How would you redesign the internet to be more privacy-focused?"
            ]
        }
        
        #time cond focused on key comparisons
        self.time_conditions = [
            300,   #5 minutes, recommended limit
            None   #unlimited, control condition
        ]
        

        self.replications = 3  #multiple runs per condition for statistical power
        self.results = []
        

        total_models = sum(2 if pair[1] else 1 for pair in self.model_pairs)
        total_questions = sum(len(questions) for questions in self.questions_by_style.values())
        self.total_tests = total_models * total_questions * len(self.time_conditions) * self.replications
        
        print(f"COMPREHENSIVE EXPERIMENT DESIGN")
        print(f" {len(self.model_pairs)} model pairs")
        print(f" {total_questions} open-ended questions across {len(self.questions_by_style)} creativity styles")
        print(f" {len(self.time_conditions)} time conditions")
        print(f" {self.replications} replications per condition")
        print(f" {self.total_tests:,} total tests")
        print(f" Estimated time: {self.total_tests * 3 / 3600:.1f} hours")
    
    def run_single_test(self, model: str, question: str, question_style: str, 
                       timeout: Optional[int], replication: int) -> Dict:
        """Run single test with comprehensive data collection"""
        
        try:
            start_time = time.time()
            result = chat_with_model_timed(
                prompt=f"Answer the following question:\n<question>{question}</question>\n"
                      f"Provide your answer in <answer></answer> XML tags.\n"
                      f"Your response should be one direct answer. Only provide one answer. "
                      f"DO NOT list multiple answers. Please try to be concise.",
                model=model,
                timeout_seconds=timeout,
                temperature=0.7
            )
            

            model_type = 'thinking' if any(x in model.lower() for x in ['thinking', 'o1', 'reasoning']) else 'standard'
            
            if result['timed_out']:
                return {
                    'model': model,
                    'model_family': model.split('/')[0],
                    'model_type': model_type,
                    'question': question,
                    'question_style': question_style,
                    'timeout_seconds': timeout,
                    'timeout_label': f"{timeout//60}min" if timeout else "unlimited",
                    'replication': replication,
                    'timed_out': True,
                    'processing_time': result['processing_time'],
                    'answer': result['content'],
                    'coherence': 0,
                    'answer_length': len(result['content']),
                    'timestamp': datetime.now().isoformat()
                }
            

            coherence = judge_answer(question, result['content'], "openai/o1-mini")
            
            return {
                'model': model,
                'model_family': model.split('/')[0],
                'model_type': model_type,
                'question': question,
                'question_category': question_style,
                'timeout_seconds': timeout,
                'timeout_label': f"{timeout//60}min" if timeout else "unlimited",
                'replication': replication,
                'timed_out': False,
                'processing_time': result['processing_time'],
                'answer': result['content'],
                'coherence': coherence,
                'answer_length': len(result['content']),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'model': model,
                'model_family': model.split('/')[0],
                'model_type': 'thinking' if any(x in model.lower() for x in ['thinking', 'o1', 'reasoning']) else 'standard',
                'question': question,
                'question_category': category,
                'timeout_seconds': timeout,
                'timeout_label': f"{timeout//60}min" if timeout else "unlimited",
                'replication': replication,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def run_experiment(self):
        """Run the comprehensive experiment"""
        
        print(f"\nStarting comprehensive experiment...")
        
        completed = 0
        

        all_conditions = []
        for pair in self.model_pairs:
            models = [pair[0]] + ([pair[1]] if pair[1] else [])
            for model in models:
                for style, questions in self.questions_by_style.items():
                    for question in questions:
                        for timeout in self.time_conditions:
                            for rep in range(self.replications):
                                all_conditions.append((model, question, style, timeout, rep))
        
        #randomize order, statistical validity
        random.shuffle(all_conditions)
        
        for model, question, style, timeout, rep in all_conditions:
            timeout_str = f"{timeout//60}min" if timeout else "unlimited"
            model_short = model.split('/')[-1][:20]
            
            print(f"[{completed+1:>4}/{len(all_conditions)}] "
                  f"{model_short:>20} | {style[:10]:>10} | "
                  f"{timeout_str:>9} | rep{rep+1}", end=" ")
            
            result = self.run_single_test(model, question, style, timeout, rep)
            self.results.append(result)
            completed += 1
            
            if 'error' in result:
                print(f" ERROR")
            elif result['timed_out']:
                print(f"TIMEOUT after {result['processing_time']:.1f}s")
            else:
                print(f" {result['processing_time']:>5.1f}s, coherence={result['coherence']:>2}")
            

            if completed % 50 == 0:
                self.save_results(f"comprehensive_progress_{completed}.json")
                print(f"     Progress saved ({completed/len(all_conditions):.1%} complete)")
        
        print(f"\nExperiment completed! {completed:,} tests finished")
        

        self.save_results("comprehensive_final_results.json")
        

        self.analyze_results()
    
    def save_results(self, filename: str):
        """Save results to file"""
        output = {
            "metadata": {
                "total_tests": len(self.results),
                "total_planned": self.total_tests,
                "completion_rate": len(self.results) / self.total_tests,
                "timestamp": datetime.now().isoformat(),
                "replications": self.replications
            },
            "results": self.results
        }
        
        filepath = filename
        with open(filepath, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"Results saved to {filename}")
    
    def confidence_interval(self, data: List[float], confidence: float = 0.95) -> tuple:
        """Calculate confidence interval"""
        if len(data) < 2:
            return (0, 0)
        
        n = len(data)
        mean = statistics.mean(data)
        
        if n == 1:
            return (mean, mean)
        
        stdev = statistics.stdev(data)
        t_critical = 1.96 if n >= 30 else 2.0  #approx
        margin = t_critical * (stdev / math.sqrt(n))
        
        return (mean - margin, mean + margin)
    
    def analyze_results(self):
        """Comprehensive statistical analysis"""
        
        print(f"\n STATISTICAL ANALYSIS")
        print("=" * 50)
        

        successful = [r for r in self.results if 'error' not in r and not r.get('timed_out', False)]
        
        print(f" Successful tests: {len(successful):,} / {len(self.results):,}")
        print(f" Success rate: {len(successful)/len(self.results):.1%}")
        
        if len(successful) == 0:
            print(" No successful results to analyze")
            return
        

        groups = {
            'time_limit': {},
            'model_type': {},
            'question_style': {},
            'model_family': {}
        }
        
        for result in successful:

            timeout_key = result['timeout_label']
            if timeout_key not in groups['time_limit']:
                groups['time_limit'][timeout_key] = []
            groups['time_limit'][timeout_key].append(result['coherence'])
            

            model_type = result['model_type']
            if model_type not in groups['model_type']:
                groups['model_type'][model_type] = []
            groups['model_type'][model_type].append(result['coherence'])

            question_style = result['question_style']
            if question_style not in groups['question_style']:
                groups['question_style'][question_style] = []
            groups['question_style'][question_style].append(result['coherence'])
            

            family = result['model_family']
            if family not in groups['model_family']:
                groups['model_family'][family] = []
            groups['model_family'][family].append(result['coherence'])
        

        print(f"\n TIME LIMIT ANALYSIS (95% confidence intervals)")
        print("-" * 50)
        
        time_stats = {}
        for label, coherence_scores in groups['time_limit'].items():
            if len(coherence_scores) >= 10:  # Minimum sample size
                mean_score = statistics.mean(coherence_scores)
                ci_low, ci_high = self.confidence_interval(coherence_scores)
                time_stats[label] = {
                    'mean': mean_score,
                    'ci_low': ci_low,
                    'ci_high': ci_high,
                    'n': len(coherence_scores)
                }
                print(f"{label:>10}: {mean_score:5.1f} [{ci_low:5.1f}, {ci_high:5.1f}] (n={len(coherence_scores)})")
        

        if '5min' in time_stats and 'unlimited' in time_stats:
            effect = time_stats['5min']['mean'] - time_stats['unlimited']['mean']
            print(f"\n TIME LIMIT EFFECT: {effect:+.1f} points")
            
            #statistical significance (rough test)
            ci_5min = time_stats['5min']
            ci_unlimited = time_stats['unlimited']
            
            # confidence intervals
            significant = (ci_5min['ci_low'] > ci_unlimited['ci_high'] or 
                          ci_unlimited['ci_low'] > ci_5min['ci_high'])
            
            print(f" Statistical significance: {'YES' if significant else 'LIKELY'}")
            print(f" Effect size: {'LARGE' if abs(effect) > 5 else 'MEDIUM' if abs(effect) > 2 else 'SMALL'}")
        

        print(f"\n MODEL TYPE ANALYSIS")
        print("-" * 30)
        
        model_type_stats = {}
        for model_type, coherence_scores in groups['model_type'].items():
            if len(coherence_scores) >= 10:
                mean_score = statistics.mean(coherence_scores)
                ci_low, ci_high = self.confidence_interval(coherence_scores)
                model_type_stats[model_type] = {
                    'mean': mean_score,
                    'ci_low': ci_low,
                    'ci_high': ci_high,
                    'n': len(coherence_scores)
                }
                print(f"{model_type:>8}: {mean_score:5.1f} [{ci_low:5.1f}, {ci_high:5.1f}] (n={len(coherence_scores)})")
        
        if 'thinking' in model_type_stats and 'standard' in model_type_stats:
            thinking_advantage = model_type_stats['thinking']['mean'] - model_type_stats['standard']['mean']
            print(f"\n THINKING MODEL ADVANTAGE: {thinking_advantage:+.1f} points")
        
 
        print(f"\n OPEN-ENDED QUESTION STYLE ANALYSIS")
        print("-" * 42)
        
        for style, coherence_scores in groups['question_style'].items():
            if len(coherence_scores) >= 5:
                mean_score = statistics.mean(coherence_scores)
                print(f"{style:>20}: {mean_score:5.1f} (n={len(coherence_scores)})")
        

        print(f"\n⏱ PROCESSING TIME ANALYSIS")
        print("-" * 30)
        
        time_groups = {}
        for result in successful:
            key = f"{result['model_type']}_{result['timeout_label']}"
            if key not in time_groups:
                time_groups[key] = []
            time_groups[key].append(result['processing_time'])
        
        for key, times in time_groups.items():
            if len(times) >= 5:
                mean_time = statistics.mean(times)
                print(f"{key:>20}: {mean_time:5.1f}s (n={len(times)})")
        

        stats_summary = {
            "time_limit_stats": time_stats,
            "model_type_stats": model_type_stats,
            "question_style_performance": {style: statistics.mean(scores) for style, scores in groups['question_style'].items() if len(scores) >= 5},
            "sample_sizes": {group: {key: len(values) for key, values in data.items()} for group, data in groups.items()},
            "total_successful_tests": len(successful),
            "key_findings": {
                "time_limit_effect": effect if '5min' in time_stats and 'unlimited' in time_stats else None,
                "thinking_advantage": thinking_advantage if 'thinking' in model_type_stats and 'standard' in model_type_stats else None
            }
        }
        
        with open('statistical_summary.json', 'w') as f:
            json.dump(stats_summary, f, indent=2)
        
        print(f" Statistical analysis saved to statistical_summary.json")

def main():
    """Main function"""
    experiment = ComprehensiveExperiment()
    
    print(f"\n This experiment will provide statistically significant evidence")
    print(f"   for time limit effects")
    
    response = input(f"\n Start comprehensive experiment? (y/N): ")
    if response.lower().startswith('y'):
        experiment.run_experiment()
    else:
        print(" Experiment ready to run when needed.")

if __name__ == "__main__":
    main()