#!/usr/bin/env python3
"""Run a transparent local coverage evaluation over the synthetic fixture."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "src"))

from smart_home_control.controller import SmartHomeController  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset", type=Path, default=Path("data/smart_home_commands_synthetic.csv")
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    with args.dataset.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))

    counts: Counter[str] = Counter()
    confusion: Counter[str] = Counter()
    for row in rows:
        decision = SmartHomeController().process(row["utterance"])
        counts["total"] += 1
        counts[f"status:{decision.status}"] += 1
        if decision.intent == row["intent"]:
            counts["intent_match"] += 1
        else:
            confusion[f"{row['intent']} -> {decision.intent}"] += 1

    report = {
        "evaluation_kind": "synthetic_coverage_check",
        "warning": "Not comparable to the historical metrics in the PDF and not a real-world accuracy estimate.",
        "dataset": str(args.dataset),
        "samples": counts["total"],
        "intent_match_rate": counts["intent_match"] / counts["total"],
        "status_counts": {
            key.removeprefix("status:"): value
            for key, value in counts.items()
            if key.startswith("status:")
        },
        "top_confusions": confusion.most_common(20),
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
