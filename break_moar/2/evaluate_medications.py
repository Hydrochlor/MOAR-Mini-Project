import json
from typing import Any, Dict
from docetl.utils_evaluation import register_eval

@register_eval
def evaluate_results(dataset_file_path: str, results_file_path: str) -> Dict[str, Any]:
    """
    Evaluate medication extraction results.

    Checks if each extracted medication appears verbatim in the original transcript.
    """
    with open(dataset_file_path, 'r', encoding='utf-8') as f:
        original_data = json.load(f)

    original_dict = {
        item.get("id", i): item.get("src", "").lower() 
        for i, item in enumerate(original_data)
    }

    with open(results_file_path, 'r', encoding='utf-8') as f:
        output = json.load(f)

    total_correct_medications = 0
    total_extracted_medications = 0

    for i, result in enumerate(output):
        item_id = result.get("id", i)
        
        true_transcript = original_dict.get(item_id, "")
        
        extracted_medications = result.get("medication", [])

        for medication in extracted_medications:
            total_extracted_medications += 1
            medication_lower = str(medication).lower().strip()

            if medication_lower in true_transcript:
                total_correct_medications += 1

    # 计算指标
    precision = total_correct_medications / total_extracted_medications if total_extracted_medications > 0 else 0.0

    return {
        "medication_extraction_score": total_correct_medications,
        "total_correct_medications": total_correct_medications,
        "total_extracted_medications": total_extracted_medications,
        "precision": precision,
    }