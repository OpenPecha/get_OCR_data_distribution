from huggingface_hub import snapshot_download
import os
import json

token = os.getenv("HUGGINGFACE_TOKEN")

def download_huggingface_repo(repo_id):
    """
    Download a Hugging Face repository.
    
    Args:
    repo_id (str): The ID of the Hugging Face repository to download.
    local_dir (str, optional): The local directory to save the repository. 
                               If not provided, it will create a directory with the repo name.
    
    Returns:downloaded_path
    str: The path to the downloaded repository.
    """
    local_dir = "./data/" + repo_id.split('/')[-1]
    os.makedirs(local_dir, exist_ok=True)
    downloaded_path = snapshot_download(repo_id=repo_id, local_dir=local_dir, token=token)
    
    print(f"Repository '{repo_id}' successfully downloaded to: {downloaded_path}")
    return downloaded_path


def get_data_distribution(download_path):
    """
    Get the data distribution of a Hugging Face repository.
    
    Args:
    repo_name (str): The name of the Hugging Face repository.
    download_path (str): The path to the downloaded repository.
    """
    data_distribution_path = os.path.join(download_path, "data.distribution")
    with open(data_distribution_path, "r") as f:
        data_distribution = f.read()
    return convert_string_to_dict(data_distribution)


def convert_string_to_dict(data_string):
    try:
        return json.loads(data_string)
    except json.JSONDecodeError:
        data_dict = {}
        lines = data_string.splitlines()
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                data_dict[key.strip()] = value.strip()
        return data_dict

def write_json(data, repo_name):
    filename = repo_name.split('/')[-1]
    with open(f'./data/{filename}.json', 'w') as f:
        json.dump(data, f, indent=4)


def main(repo_names):
    for repo_name in repo_names:
        download_path = download_huggingface_repo(repo_name)
        data_distribution = get_data_distribution(download_path)
        write_json(data_distribution, repo_name)


def get_data_distribution():
    filenames = ['dergetenjur_data.distribution', 'lhasakanjur_data.distribution', 'lithangkanjur_data.distribution']
    for filename in filenames:
        file_path = f"./data/{filename}"
        with open(file_path, "r") as f:
            data_distribution = f.read()
            data_dict = convert_string_to_dict(data_distribution)
            write_json(data_dict, filename.split(".")[0])



if __name__ == "__main__":
    get_data_distribution()