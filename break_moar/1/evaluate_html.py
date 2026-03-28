import json
import re
from typing import Any, Dict
from docetl.utils_evaluation import register_eval

@register_eval
def evaluate_results(dataset_file_path: str, results_file_path: str) -> Dict[str, Any]:
    with open(results_file_path, 'r', encoding='utf-8') as f:
        output = json.load(f)

    correct_count = 0

    for result in output:
        raw_html = result.get("raw_html", "")
        extracted_text = result.get("clean_text", "")
        
        true_text = re.sub(r'<[^>]+>', ' ', raw_html)
        true_text = re.sub(r'\s+', ' ', true_text).strip()
        
        normalized_extracted = re.sub(r'\s+', ' ', extracted_text).strip()

        if normalized_extracted == true_text:
            correct_count += 1

    return {"html_clean_score": correct_count}