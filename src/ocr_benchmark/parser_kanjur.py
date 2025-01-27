import json
import os
import pyewts

converter = pyewts.pyewts()


def is_wylie(text):
    try:
        converted = converter.toUnicode(text)
        return True if converted else False
    except Exception:
        return False


def convert_to_unicode(label):
    if is_wylie(label):
        return converter.toUnicode(label)
    return label


def generate_image_url(filename):
    base_url = "https://s3.amazonaws.com/monlam.ai.ocr/lhasa_kanjur/"
    return f"{base_url}{filename}.jpg"


def process_json_line(data):
    data["label"] = convert_to_unicode(data["label"])
    filename = data["filename"]
    data["image_url"] = generate_image_url(filename)
    data["BDRC_work_id"] = "W23703"
    data["char_len"] = len(data["label"])
    data["script"] = "ScriptTibt"
    data["writing_style"] = "Uchan"
    data["print_method"] = "PrintMethod_Woodblock"
    return data


def process_jsonl_file(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as infile, open(
        output_file, "w", encoding="utf-8"
    ) as outfile:
        for line in infile:
            data = json.loads(line)
            updated_data = process_json_line(data)
            outfile.write(json.dumps(updated_data, ensure_ascii=False) + "\n")


def process_directory(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".jsonl"):
                input_file_path = os.path.join(root, file)

                relative_path = os.path.relpath(root, input_dir)
                output_folder = os.path.join(output_dir, relative_path)
                os.makedirs(output_folder, exist_ok=True)

                output_file_path = os.path.join(output_folder, file)
                process_jsonl_file(input_file_path, output_file_path)
                print(f"Processed: {input_file_path} -> {output_file_path}")


if __name__ == "__main__":
    input_directory = "data/add_metadata/jsonl_source_repo/lithang_kanjur"
    output_directory = "data/add_metadata/output_jsonl/lithang_kanjur"

    process_directory(input_directory, output_directory)
