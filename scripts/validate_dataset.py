#!/usr/bin/env python3
"""Validate schema, provenance, JSON payloads, and reported class totals."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from generate_dataset import validate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path", nargs="?", type=Path, default=Path("data/smart_home_commands_synthetic.csv")
    )
    args = parser.parse_args()
    with args.path.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    validate(rows)
    for row in rows:
        assert row["source"] == "synthetic_template_v1"
        assert row["privacy"] == "contains_no_real_user_data"
        commands = json.loads(row["expected_commands_json"])
        assert isinstance(commands, list)
    print(f"dataset valid: {len(rows)} rows")


if __name__ == "__main__":
    main()
