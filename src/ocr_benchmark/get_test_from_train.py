import json
import os


def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def load_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [json.loads(line.strip()) for line in file]


def save_jsonl(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for entry in data:
            file.write(json.dumps(entry, ensure_ascii=False) + '\n')


def filter_train_json(data_distribution_path, train_jsonl_path, output_path):

    data_distri_json = load_json(data_distribution_path)
    train_jsonl = load_jsonl(train_jsonl_path)
    test_images = set(data_distri_json.get('test', []))

    filtered_data = [
        entry for entry in train_jsonl
        if os.path.splitext(entry.get('filename', ''))[0] in test_images
    ]

    save_jsonl(filtered_data, output_path)
    print(f"Filtered data saved to {output_path}")


data_distribution_path = 'data/data_distribution/drutsa.json'  
train_jsonl_path = 'data/test_data_json/OCR-Drutsa_train.jsonl'  
output_path = 'data/test_data_json/OCR-Drutsa.jsonl'

filter_train_json(data_distribution_path, train_jsonl_path, output_path)
