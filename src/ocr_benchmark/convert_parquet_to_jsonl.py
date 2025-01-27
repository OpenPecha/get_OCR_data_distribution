import pandas as pd
import json
import os


def convert_to_jsonl(df, output_path):
    with open(output_path, "w", encoding="utf-8") as jsonl_file:
        for record in df.to_dict(orient="records"):
            json.dump(record, jsonl_file, ensure_ascii=False)
            jsonl_file.write("\n")


def convert_parquet_to_jsonl(input_dir, output_dir):
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".parquet"):
                input_file_path = os.path.join(root, file)

                relative_path = os.path.relpath(root, input_dir)
                output_folder = os.path.join(output_dir, relative_path)
                os.makedirs(output_folder, exist_ok=True)

                output_file_path = os.path.join(
                    output_folder, os.path.splitext(file)[0] + ".jsonl"
                )

                df = pd.read_parquet(input_file_path)
                convert_to_jsonl(df, output_file_path)
                print(f"Converted: {input_file_path} -> {output_file_path}")


def main():
    input_directory = "data/add_metadata/source_repo"
    output_directory = "data/add_metadata/jsonl_source_repo"
    convert_parquet_to_jsonl(input_directory, output_directory)


if __name__ == "__main__":
    main()
