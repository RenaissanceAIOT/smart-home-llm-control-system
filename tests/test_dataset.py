import csv
import json
from collections import Counter
from pathlib import Path


def test_committed_dataset_contract() -> None:
    path = Path(__file__).parents[1] / "data" / "smart_home_commands_synthetic.csv"
    with path.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 1119
    assert Counter(row["instruction_type"] for row in rows) == {
        "explicit": 526,
        "implicit": 593,
    }
    assert all(row["source"] == "synthetic_template_v1" for row in rows)
    assert all(isinstance(json.loads(row["expected_commands_json"]), list) for row in rows)
