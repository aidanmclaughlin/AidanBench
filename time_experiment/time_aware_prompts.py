#creating time aware prompts to tell models upfront how much time they have
#tested qs are openended creativity questions in diff flavours

import re
from time_aware_models import chat_with_model_timed


def gen_answer_with_time_limit(question: str, previous_answers: list, model_name: str, timeout_seconds: int = None) -> str:
    """Generate answer with time awareness and (optional) timeout"""
    
    #letting them know their time constraint to try to stop overthinking or wordiness. do they know what time means? 
    if timeout_seconds:
        time_info = f"\n**IMPORTANT: You have {timeout_seconds} seconds to provide a complete answer. Budget your time accordingly and ensure you give a substantive response within this limit.**\n"
    else:
        time_info = "\n**You have unlimited time for this response.**\n"
    
    base_prompt = (
        "Answer the following question:\n"
        "<question>" + question + "</question>\n" +
        time_info +
        "Provide your answer in <answer></answer> XML tags.\n"
    )

    base_prompt += "Your response should be one direct answer. Only provide one answer. DO NOT list multiple answers. Please try to be concise.\n"

    if previous_answers:
        previous_answers_str = "\n\n".join(
            [f"<previous_answer id='{i+1}'>\n{answer}\n</previous_answer>" for i, answer in enumerate(previous_answers)]
        )
        base_prompt += (
            "IMPORTANT: Provide an answer you *HAVE NOT* given previously.\n"
            "Your previous answers are inside of <previous_answers></previous_answers> XML tags.\n"
            "<previous_answers>\n" + previous_answers_str + "\n</previous_answers>"
        )

    response_data = chat_with_model_timed(
        base_prompt, 
        model=model_name, 
        temperature=0.7, 
        timeout_seconds=timeout_seconds
    )
    
    answer_text = _extract_xml_content(response_data['content'], "answer")
    
    return {
        'answer': answer_text,
        'processing_time': response_data['processing_time'],
        'timed_out': response_data['timed_out'],
        'timeout_limit': response_data['timeout_limit']
    }


def judge_answer(question: str, answer: str, model_name: str) -> int:
    prompt = (
        "Your task is to evaluate the coherence and plausibility of an answer to a given question.\n\n"
        "Question: <question>" + question + "</question>\n"
        "Answer: <answer>" + answer + "</answer>\n\n"
        "Based on the following criteria, provide a Coherence and Plausibility Score on a scale of 0 - 100:\n\n"
        "0-20: INCOHERENT/NONSENSICAL\n"
        "21-40: SEVERELY FLAWED\n"
        "41-60: PARTIALLY COHERENT\n"
        "61-80: MOSTLY COHERENT\n"
        "81-100: HIGHLY COHERENT\n\n"
        "IMPORTANT: Provide your final Coherence and Plausibility Score as a single integer between 0 and 100, "
        "enclosed in <coherence_score></coherence_score> XML tags.\n\n"
        "Do not include any additional text in your response."
    )
    response_data = chat_with_model_timed(prompt, model="o1-mini")
    return int(_extract_xml_content(response_data['content'], "coherence_score"))


def _extract_xml_content(text: str, tag: str) -> str:
    """Extract content from XML tags"""
    pattern = f"<{tag}>(.*?)</{tag}>"
    matches = re.findall(pattern, text, re.DOTALL)
    return matches[-1].strip() if matches else text