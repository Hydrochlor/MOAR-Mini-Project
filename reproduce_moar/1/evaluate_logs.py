import json
import re
from typing import Any, Dict
from docetl.utils_evaluation import register_eval

@register_eval
def evaluate_results(dataset_file_path: str, results_file_path: str) -> Dict[str, Any]:
    with open(results_file_path, 'r', encoding='utf-8') as f:
        output = json.load(f)

    correct_count = 0
    ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

    for result in output:
        log_text = result.get("log", "")
        extracted_ips = result.get("ip_address", [])
        
        true_ips = ip_pattern.findall(log_text)

        if set(extracted_ips) == set(true_ips):
            correct_count += 1

    return {"ip_extraction_score": correct_count}