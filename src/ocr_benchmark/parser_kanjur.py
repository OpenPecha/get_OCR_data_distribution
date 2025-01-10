import json
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
    base_url = "https://s3.amazonaws.com/monlam.ai.ocr/OCR-Benchmark/OCR-LhasaKanjur/"
    return f"{base_url}{filename}.jpg"


def process_json_line(data):
    """Process a single JSON object, adding new key-value pairs."""
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
    with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
        for line in infile:
            data = json.loads(line)
            updated_data = process_json_line(data)
            outfile.write(json.dumps(updated_data, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    input_file = "data/test_data_json/OCR-Lhasakanjur.jsonl"
    output_file = "data/ocr_bm_data_jsonl/Lhasa_Kanjur.jsonl"

    process_jsonl_file(input_file, output_file)
