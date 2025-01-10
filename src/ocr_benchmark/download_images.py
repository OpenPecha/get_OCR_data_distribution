import os
import json
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor


def download_image(url, save_path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Image saved to {save_path}")
        else:
            print(f"Failed to download {url}: HTTP {response.status_code}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")


def process_jsonl_file(jsonl_file, output_dir):
    jsonl_name = Path(jsonl_file).stem
    folder_path = os.path.join(output_dir, jsonl_name)
    os.makedirs(folder_path, exist_ok=True)

    tasks = []

    with open(jsonl_file, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                data = json.loads(line.strip())
                if "image_url" in data and data["image_url"].startswith("https://"):
                    image_url = data["image_url"]
                    image_name = os.path.basename(image_url)
                    save_path = os.path.join(folder_path, image_name)
                    tasks.append((image_url, save_path))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in {jsonl_file}: {e}")
            except Exception as e:
                print(f"Error processing line in {jsonl_file}: {e}")

    with ThreadPoolExecutor() as executor:
        for url, save_path in tasks:
            executor.submit(download_image, url, save_path)


def main():
    jsonl_file = "data/test_data_json/OCR-Dergetenjur.jsonl"  
    output_dir = "data/ocr_benchmark_images"    
    print(f"Processing file: {jsonl_file}")
    process_jsonl_file(jsonl_file, output_dir)


if __name__ == "__main__":
    main()
