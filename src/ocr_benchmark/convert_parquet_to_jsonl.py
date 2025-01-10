import pandas as pd
import json
import os


def convert_to_jsonl(df, output_path):
    with open(output_path, 'w', encoding='utf-8') as jsonl_file:
        for record in df.to_dict(orient="records"):
            json.dump(record, jsonl_file, ensure_ascii=False)
            jsonl_file.write('\n')


input_file = 'data/OCR-Derge_Tenjur.parquet'
output_file = 'data/test_data_json/OCR-Dergetenjur.jsonl'

os.makedirs(os.path.dirname(output_file), exist_ok=True)
df = pd.read_parquet(input_file)
convert_to_jsonl(df, output_file)

print(f"Converted {input_file} to {output_file}")
