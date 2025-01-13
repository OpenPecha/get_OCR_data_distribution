import os
import pandas as pd
from datasets import Dataset, DatasetDict
from huggingface_hub import HfApi


local_dir = "../data/ocr_bm_data_jsonl"
repo_name = "openpecha/OCR-Tibetan_line_to_text_benchmark"


def convert_jsonl_to_parquet(local_dir):
    datasets_dict = {}

    for file_name in os.listdir(local_dir):
        if file_name.endswith(".jsonl"):
            jsonl_path = os.path.join(local_dir, file_name)

            df = pd.read_json(jsonl_path, lines=True)
            if "filename" in df.columns:
                df["filename"] = df["filename"].astype(str)
            parquet_file = jsonl_path.replace(".jsonl", ".parquet")
            df.to_parquet(parquet_file, engine="pyarrow")

            dataset = Dataset.from_pandas(df)
            split_name = file_name.replace(".jsonl", "")
            datasets_dict[split_name] = dataset

    return DatasetDict(datasets_dict)


def upload_to_huggingface(dataset_dict, repo_name):
    api = HfApi()
    try:
        api.create_repo(repo_name, repo_type="dataset")
    except Exception as e:
        print(f"Repo already exists: {e}")
    dataset_dict.push_to_hub(repo_name, token=True)


dataset_dict = convert_jsonl_to_parquet(local_dir)
upload_to_huggingface(dataset_dict, repo_name)
