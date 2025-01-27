import os
import json


def process_jsonl(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as infile, open(
        output_file, "w", encoding="utf-8"
    ) as outfile:
        for line in infile:
            data = json.loads(line.strip())

            restructured_data = {
                "filename": str(data["filename"]),
                "label": data["label"],
                "image_url": data["image_url"],
                "BDRC_work_id": "",
                "char_len": len(data["label"]),
                "script": "ScriptUmed",
                "writing_style": "Betsug",
                "print_method": "PrintMethod_Woodblock",
            }

            outfile.write(json.dumps(restructured_data, ensure_ascii=False) + "\n")


def process_directory(input_dir, output_dir):
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".jsonl"):
                input_file_path = os.path.join(root, file)

                relative_path = os.path.relpath(root, input_dir)
                output_folder = os.path.join(output_dir, relative_path)
                os.makedirs(output_folder, exist_ok=True)

                output_file_path = os.path.join(output_folder, file)
                process_jsonl(input_file_path, output_file_path)
                print(f"Processed: {input_file_path} -> {output_file_path}")


if __name__ == "__main__":
    input_directory = "data/add_metadata/jsonl_source_repo/dergetenjur"
    output_directory = "data/add_metadata/output_jsonl/derge_tenjur"
    process_directory(input_directory, output_directory)
