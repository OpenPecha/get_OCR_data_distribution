import os
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from datasets import DatasetDict, Dataset
from src.ocr_benchmark.create_hf_repo_from_json import convert_jsonl_to_parquet, upload_to_huggingface


@pytest.fixture
def mock_local_dir(tmpdir):
    local_dir = tmpdir.mkdir("ocr_bm_data_jsonl")
    sample_data = [
        {"text": "Sample text 1", "filename": "file1.jsonl"},
        {"text": "Sample text 2", "filename": "file2.jsonl"},
    ]
    jsonl_path = local_dir.join("train.jsonl")
    pd.DataFrame(sample_data).to_json(jsonl_path, orient="records", lines=True)
    return str(local_dir)


def test_convert_jsonl_to_parquet(mock_local_dir):
    dataset_dict = convert_jsonl_to_parquet(mock_local_dir)
    assert isinstance(dataset_dict, DatasetDict)
    assert "train" in dataset_dict
    assert isinstance(dataset_dict["train"], Dataset)
    parquet_path = os.path.join(mock_local_dir, "train.parquet")
    assert os.path.exists(parquet_path)
    dataset = dataset_dict["train"]
    assert len(dataset) == 2
    assert dataset[0]["text"] == "Sample text 1"
    assert dataset[0]["filename"] == "file1.jsonl"


@patch("src.ocr_benchmark.create_hf_repo_from_json.HfApi")
@patch.object(DatasetDict, "push_to_hub", autospec=True)
def test_upload_to_huggingface(mock_push_to_hub, mock_hfapi):
    mock_hfapi_instance = MagicMock()
    mock_hfapi.return_value = mock_hfapi_instance
    data = {"text": ["Sample text"], "filename": ["file1.jsonl"]}
    mock_dataset_dict = DatasetDict({"train": Dataset.from_pandas(pd.DataFrame(data))})

    repo_name = "test_repo"
    upload_to_huggingface(mock_dataset_dict, repo_name)

    mock_hfapi_instance.create_repo.assert_called_once_with(repo_name, repo_type="dataset")
    mock_push_to_hub.assert_called_once_with(mock_dataset_dict, repo_name, token=True)
