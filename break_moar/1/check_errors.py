import json
import re

def check_html_errors(original_data_file, result_file):
    with open(original_data_file, 'r', encoding='utf-8') as f:
        original_data = {item['id']: item['raw_html'] for item in json.load(f)}

    with open(result_file, 'r', encoding='utf-8') as f:
            results = json.load(f)

    error_count = 0

    for res in results:
        item_id = res.get('id')
        
        true_raw_html = original_data.get(item_id, "")
        extracted_text = res.get('clean_text', "")

        true_text = re.sub(r'<[^>]+>', ' ', true_raw_html)
        true_text = re.sub(r'\s+', ' ', true_text).strip()

        normalized_extracted = re.sub(r'\s+', ' ', str(extracted_text)).strip()

        if normalized_extracted != true_text:
            error_count += 1
            print(f"ID: {item_id}")
            print(f"Original HTML: {true_raw_html}")
            print(f"Ground Truth: '{true_text}'")
            print(f"Output: '{normalized_extracted}'")
            print("-" * 70)

    print(f"\nTotal error counts: {error_count}")

if __name__ == "__main__":
    original_file = "html_data.json"
    
    node_file = "results/moar_optimization_html/pipeline_6.json"
    
    check_html_errors(original_file, node_file)