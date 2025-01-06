import os
import pandas as pd
import json


def write_jsonl_with_tibetan(df, output_path):
    with open(output_path, 'w', encoding='utf-8') as jsonl_file:
        for record in df.to_dict(orient="records"):
            json.dump(record, jsonl_file, ensure_ascii=False)
            jsonl_file.write('\n')


input_dir = 'data/test_data'
output_dir = 'data/test_data_json'

os.makedirs(output_dir, exist_ok=True)


for file_name in os.listdir(input_dir):
    if file_name.endswith('.parquet'):
        input_path = os.path.join(input_dir, file_name)
        output_path = os.path.join(output_dir, file_name.replace('.parquet', '.jsonl'))
        df = pd.read_parquet(input_path)

        write_jsonl_with_tibetan(df, output_path)

        print(f"Converted {file_name} to {output_path}")
