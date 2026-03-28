import json
import re
from typing import Any, Dict
from docetl.utils_evaluation import register_eval

def normalize_text(text: str):
    text = str(text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)
    return text.strip()

@register_eval
def evaluate_results(dataset_file_path: str, results_file_path: str) -> Dict[str, Any]:
    with open(dataset_file_path, 'r', encoding='utf-8') as f:
        original_data = json.load(f)
        
    original_dict = {item.get("id"): item.get("raw_html", "") for item in original_data}

    with open(results_file_path, 'r', encoding='utf-8') as f:
        output = json.load(f)

    correct_count = 0

    for result in output:
        item_id = result.get("id")
        
        true_raw_html = original_dict.get(item_id, "") 
        
        extracted_text = result.get("clean_text", "")
        
        true_text = re.sub(r'<[^>]+>', ' ', true_raw_html)
        
        normalized_true = normalize_text(true_text)
        normalized_extracted = normalize_text(extracted_text)

        if normalized_extracted == normalized_true:
            correct_count += 1

    return {"html_clean_score": correct_count}