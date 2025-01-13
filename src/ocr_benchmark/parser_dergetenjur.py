import json

input_file = "data/test_data_json/OCR-Dergetenjur.jsonl"
output_file = "data/ocr_bm_data_jsonl/Derge_Tenjur.jsonl"


def process_jsonl(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
        for line in infile:
            data = json.loads(line.strip())

            restructured_data = {
                "filename": str(data["filename"]),
                "label": data["label"],
                "image_url": data["image_url"],
                "BDRC_work_id": "W23703",
                "char_len": len(data["label"]),
                "script": "ScriptTibt",
                "writing_style": "Uchan",
                "print_method": "PrintMethod_Woodblock"
            }

            outfile.write(json.dumps(restructured_data, ensure_ascii=False) + "\n")


process_jsonl(input_file, output_file)
