from pathlib import Path
import json

def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


def test_data():
    Norbuketaka_path = Path("data/Norbuketaka_C_V1.json")
    Norbuketaka = read_json(Norbuketaka_path)
    assert len(Norbuketaka['train']) == 1808695
    assert len(Norbuketaka['validation']) == 223808
    assert len(Norbuketaka['test']) == 223080