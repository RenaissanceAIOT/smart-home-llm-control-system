#!/usr/bin/env python3
"""Generate the transparent 1,119-row synthetic coverage dataset.

This dataset reproduces the class totals reported in the project PDF, not the
missing original user records. Templates, seed, schema, and provenance are
committed so every row can be independently regenerated.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from collections import Counter
from pathlib import Path
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "src"))

from smart_home_control.catalog import DEVICE_CATALOG  # noqa: E402
from smart_home_control.domain import Command, IntentResult  # noqa: E402
from smart_home_control.planner import commands_for_intent  # noqa: E402

SEED = 20260606
EXPLICIT_COUNTS = {
    "lighting": 211,
    "kitchen_bath": 173,
    "climate": 78,
    "door_window": 32,
    "curtain": 19,
    "appliance": 9,
    "media": 3,
    "security": 1,
}
IMPLICIT_COUNTS = {
    "lighting": 171,
    "kitchen_bath": 188,
    "climate": 93,
    "door_window": 45,
    "curtain": 33,
    "appliance": 24,
    "media": 22,
    "security": 17,
}
PARAMETER_COUNTS = {"lighting": 60, "kitchen_bath": 10, "climate": 35, "curtain": 9}
SUBTYPE_COUNTS = {"sensation": 287, "scene": 236, "health": 70}

EXPLICIT_PREFIXES = ("请", "麻烦", "现在", "帮我", "可以帮我")
EXPLICIT_ENDINGS = ("", "一下", "吧", "谢谢", "现在就执行")

IMPLICIT_CASES: dict[str, tuple[tuple[str, tuple[str, ...]], ...]] = {
    "lighting": (
        ("brighten", ("屋里太暗了，看不清东西", "光线有点暗，我要看书", "这里黑乎乎的")),
        ("sleep_mode", ("准备睡觉了", "晚安，我要休息了")),
    ),
    "kitchen_bath": (
        ("bath_preparation", ("我要洗澡了", "准备冲个热水澡", "下班了想先沐浴")),
        ("cooking_mode", ("准备做饭了", "我要开始炒菜", "晚餐时间到了")),
    ),
    "climate": (
        ("cool_down", ("今天好热", "屋里有点闷热", "想凉快一点")),
        ("warm_up", ("我好冷", "屋里冷飕飕的", "想暖和一点")),
    ),
    "door_window": (("ventilate", ("屋里闷得慌，想透透气", "空气不流通", "让房间通通风")),),
    "curtain": (
        ("wake_up_mode", ("早安，该起床了", "天亮了，我要起床", "新的一天开始了")),
        ("sleep_mode", ("我要睡觉了", "该休息了，晚安")),
    ),
    "appliance": (
        ("humidify", ("空气太干了", "嗓子有点干", "屋里需要加点湿度")),
        ("purify_air", ("空气有异味", "屋里空气不好", "想呼吸干净空气")),
        ("cleaning_mode", ("地上有灰，该打扫了", "家里需要清扫一下")),
    ),
    "media": (("relax_mode", ("想看电影放松一下", "今晚追个剧吧", "我想在客厅休息一会")),),
    "security": (("leave_home_mode", ("我准备出门上班", "家里没人了", "我要离家一会")),),
}


def _command_payload(commands: list[Command]) -> str:
    return json.dumps(
        [command.to_dict() for command in commands], ensure_ascii=False, separators=(",", ":")
    )


def _parameter_command(category: str, index: int) -> tuple[Any, Command, str]:
    choices = {
        "lighting": [
            d
            for d in DEVICE_CATALOG
            if d.category == category and "set_brightness" in d.capabilities
        ],
        "climate": [
            d
            for d in DEVICE_CATALOG
            if d.category == category and "set_temperature" in d.capabilities
        ],
        "kitchen_bath": [d for d in DEVICE_CATALOG if "set_water_temperature" in d.capabilities],
        "curtain": [
            d for d in DEVICE_CATALOG if d.category == category and "set_position" in d.capabilities
        ],
    }[category]
    device = choices[index % len(choices)]
    if category == "lighting":
        value = 10 + (index * 10) % 90
        return (
            device,
            Command(device.device_id, "set_brightness", {"brightness": value}),
            f"把{device.name}亮度调到{value}%",
        )
    if category == "climate":
        value = 18 + index % 11
        return (
            device,
            Command(device.device_id, "set_temperature", {"temperature": value}),
            f"把{device.name}温度调到{value}度",
        )
    if category == "kitchen_bath":
        value = 38 + index % 16
        return (
            device,
            Command(device.device_id, "set_water_temperature", {"water_temperature": value}),
            f"把{device.name}温度调到{value}度",
        )
    value = 10 + (index * 10) % 90
    return (
        device,
        Command(device.device_id, "set_position", {"position": value}),
        f"把{device.name}位置调到{value}%",
    )


def _switch_command(category: str, index: int) -> tuple[Any, Command, str]:
    devices = [device for device in DEVICE_CATALOG if device.category == category]
    device = devices[index % len(devices)]
    if category == "security":
        action, phrase = "lock", f"锁上{device.name}"
    elif "turn_on" in device.capabilities:
        action = "turn_on" if index % 2 == 0 else "turn_off"
        phrase = ("打开" if action == "turn_on" else "关闭") + device.name
    elif "open" in device.capabilities:
        action = "open" if index % 2 == 0 else "close"
        phrase = ("打开" if action == "open" else "关闭") + device.name
    else:
        action = device.capabilities[0]
        phrase = f"让{device.name}执行{action}"
    return device, Command(device.device_id, action), phrase


def _row(
    row_id: int,
    *,
    utterance: str,
    instruction_type: str,
    subtype: str,
    intent: str,
    primary_device: Any,
    commands: list[Command],
) -> dict[str, str]:
    split_bucket = row_id % 10
    split = "train" if split_bucket < 8 else "validation" if split_bucket == 8 else "test"
    return {
        "sample_id": f"SHC-{row_id:04d}",
        "utterance": utterance,
        "instruction_type": instruction_type,
        "subtype": subtype,
        "intent": intent,
        "room": primary_device.room,
        "primary_device_id": primary_device.device_id,
        "primary_device_name": primary_device.name,
        "device_category": primary_device.category,
        "expected_commands_json": _command_payload(commands),
        "split": split,
        "source": "synthetic_template_v1",
        "privacy": "contains_no_real_user_data",
    }


def generate() -> list[dict[str, str]]:
    rng = random.Random(SEED)
    rows: list[dict[str, str]] = []
    row_id = 1
    for category, count in EXPLICIT_COUNTS.items():
        parameter_count = PARAMETER_COUNTS.get(category, 0)
        for index in range(count):
            if index < parameter_count:
                device, command, core = _parameter_command(category, index)
                subtype = "parameter"
            else:
                device, command, core = _switch_command(category, index - parameter_count)
                subtype = "switch"
            utterance = f"{rng.choice(EXPLICIT_PREFIXES)}{core}{rng.choice(EXPLICIT_ENDINGS)}"
            rows.append(
                _row(
                    row_id,
                    utterance=utterance,
                    instruction_type="explicit",
                    subtype=subtype,
                    intent="explicit_control",
                    primary_device=device,
                    commands=[command],
                )
            )
            row_id += 1

    subtype_queue = [subtype for subtype, count in SUBTYPE_COUNTS.items() for _ in range(count)]
    rng.shuffle(subtype_queue)
    for category, count in IMPLICIT_COUNTS.items():
        category_devices = [device for device in DEVICE_CATALOG if device.category == category]
        cases = IMPLICIT_CASES[category]
        for index in range(count):
            subtype = subtype_queue.pop()
            intent_name, templates = cases[index % len(cases)]
            utterance = templates[(index // len(cases)) % len(templates)]
            if subtype == "health":
                utterance += rng.choice(("，我最近有点感冒", "，家里有老人", "，嗓子不太舒服"))
            elif subtype == "scene":
                utterance += rng.choice(("，帮我准备一下", "，现在开始吧", "，按平时的习惯来"))
            else:
                utterance += rng.choice(("", "，有点不舒服", "，能改善一下吗"))
            primary_device = category_devices[index % len(category_devices)]
            commands = commands_for_intent(
                IntentResult(intent_name, 1.0, "dataset-label"), utterance
            )
            rows.append(
                _row(
                    row_id,
                    utterance=utterance,
                    instruction_type="implicit",
                    subtype=subtype,
                    intent=intent_name,
                    primary_device=primary_device,
                    commands=commands,
                )
            )
            row_id += 1
    assert not subtype_queue
    return rows


def validate(rows: list[dict[str, str]]) -> None:
    assert len(rows) == 1119
    type_counts = Counter(row["instruction_type"] for row in rows)
    assert type_counts == {"explicit": 526, "implicit": 593}
    for instruction_type, expected in (
        ("explicit", EXPLICIT_COUNTS),
        ("implicit", IMPLICIT_COUNTS),
    ):
        actual = Counter(
            row["device_category"] for row in rows if row["instruction_type"] == instruction_type
        )
        assert actual == expected
    assert Counter(row["subtype"] for row in rows if row["instruction_type"] == "explicit") == {
        "switch": 412,
        "parameter": 114,
    }
    assert (
        Counter(row["subtype"] for row in rows if row["instruction_type"] == "implicit")
        == SUBTYPE_COUNTS
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path, default=Path("data/smart_home_commands_synthetic.csv")
    )
    parser.add_argument("--summary", type=Path, default=Path("data/dataset_summary.json"))
    args = parser.parse_args()
    rows = generate()
    validate(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "name": "smart_home_commands_synthetic",
        "version": "1.0.0",
        "seed": SEED,
        "rows": len(rows),
        "provenance": "synthetic; generated from committed templates; no real user data",
        "instruction_type": dict(Counter(row["instruction_type"] for row in rows)),
        "subtype": dict(Counter(row["subtype"] for row in rows)),
        "device_category": dict(Counter(row["device_category"] for row in rows)),
        "split": dict(Counter(row["split"] for row in rows)),
    }
    args.summary.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
