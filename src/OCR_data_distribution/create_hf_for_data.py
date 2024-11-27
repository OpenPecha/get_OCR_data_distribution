from pathlib import Path
import os
import json
import shutil
import pyarrow as pa
from pathlib import Path
import pandas as pd
from datasets import Dataset, DatasetDict
import os
from huggingface_hub import HfApi


data_name = "lithang_kanjur"
token = os.getenv("HUGGINGFACE_TOKEN")
zip_dir = Path(f"./data/{data_name}")
images_dir = Path(f"/Users/tashitsering/Desktop/work/OCR-data-consolidation/data/{data_name}/lines")
text_dir = Path(f"/Users/tashitsering/Desktop/work/OCR-data-consolidation/data/{data_name}/transcriptions")
text_csv = Path(f"/Users/tashitsering/Desktop/work/OCR-data-consolidation/data/csv/{data_name}.csv")
image_text_dict = {}
    
def upload_zip(zip_file, repo_id):
    api = HfApi()
    api.upload_file(
        path_or_fileobj=zip_file,
        path_in_repo=Path(zip_file).name,
        repo_id=repo_id,
        repo_type='dataset',
        token=token
    )

    print(f"Parquet datasets and zip file uploaded successfully to repo: {repo_id}")
    shutil.rmtree(zip_dir)


def create_parquet(train_df, eval_df, test_df, zip_file, repo_id, token):
    # Save the DataFrames as Parquet files
    train_df.to_parquet('train.parquet', engine='pyarrow')
    eval_df.to_parquet('eval.parquet', engine='pyarrow')
    test_df.to_parquet('test.parquet', engine='pyarrow')

    # Load the Parquet files as Hugging Face datasets
    train_dataset = Dataset.from_pandas(pd.read_parquet('train.parquet'))
    eval_dataset = Dataset.from_pandas(pd.read_parquet('eval.parquet'))
    test_dataset = Dataset.from_pandas(pd.read_parquet('test.parquet'))

    # Combine them into a DatasetDict
    dataset_dict = DatasetDict({
        'train': train_dataset,
        'eval': eval_dataset,
        'test': test_dataset
    })

    # Push the datasets to the Hugging Face Hub
    dataset_dict.push_to_hub(repo_id=repo_id, token=token)
    upload_zip(zip_file, repo_id)


def read_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def get_data_split(json_path):
    data_json = read_json(json_path)
    training_images = data_json["training_images"]
    validation_images = data_json["validation_images"]
    test_images = data_json["test_images"]

    return training_images, validation_images, test_images


def get_all_images_paths(images_dir):
    images_paths = list(images_dir.iterdir())
    return images_paths


def get_text(image):
    global image_text_dict
    if text_csv.exists():
        if len(image_text_dict) == 0:
            df = pd.read_csv(text_csv)
            image_text_dict = dict(zip(df['image_name'], df['label']))
            try:
                text = image_text_dict[f"{image}.jpg"]
                return text
            except KeyError:
                print(f"Text for image {image} not found in the csv file.")
                return
    else:
        return Path(f"{text_dir}/{image}.txt").read_text(encoding='utf-8')
        

def get_data_df(images):
    texts = []
    for image in images:
        image_path = Path(f"{images_dir}/{image}.jpg")
        if image_path.exists():
            text = Path(f"{text_dir}/{image}.txt").read_text(encoding='utf-8')
            filename = image
            label = text
            texts.append((filename, label))
            zip_path = Path(f"{zip_dir}/{image}.jpg")
            if zip_path.exists():
                continue            
            shutil.copy(image_path, zip_path)
        else:
            print(f"Image {image} not found in the data distribution.")
    df = pd.DataFrame(texts, columns=['filename', 'label'])
    return df


def get_dfs(json_path):
    data_json = read_json(json_path)
    train_df = get_data_df(data_json["train"])
    eval_df = get_data_df(data_json["validation"])
    test_df = get_data_df(data_json["test"])
    return train_df, eval_df, test_df


def compress_dir(output_path):
    shutil.make_archive(output_path, 'zip', output_path)
    print(f"Directory '{output_path}' successfully zipped to: {output_path}.zip")
    return f"{output_path}.zip"

def main():
    repo_id = "openpecha/OCR-Lithangkanjur"
    json_path = Path(f"./data/Lithangkanjur_data.json")
    train_df, eval_df, test_df = get_dfs(json_path)
    zip_file = compress_dir(zip_dir)
    create_parquet(train_df, eval_df, test_df, zip_file, repo_id, token)


if __name__ == "__main__":
    main()