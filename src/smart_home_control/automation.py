"""Simple persistent schedule memory backed by SQLite."""

from __future__ import annotations

import json
import re
import sqlite3
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

from .domain import Command
from .intents import HybridIntentClassifier, normalize_text
from .planner import commands_for_intent


@dataclass(frozen=True, slots=True)
class Automation:
    automation_id: str
    title: str
    schedule: str
    hour: int
    minute: int
    source_text: str
    commands: tuple[Command, ...]
    enabled: bool = True


def parse_automation(text: str) -> Automation | None:
    normalized = normalize_text(text)
    match = re.search(r"(\d{1,2})(?:[:点时](\d{1,2})?分?)", normalized)
    if not match:
        return None
    hour = int(match.group(1))
    minute = int(match.group(2) or 0)
    if not 0 <= hour <= 23 or not 0 <= minute <= 59:
        return None
    schedule = (
        "weekdays" if "工作日" in normalized else "weekends" if "周末" in normalized else "daily"
    )
    stripped = re.sub(r"(每天|每晚|每周|工作日|周末|定时|自动)", "", normalized)
    stripped = re.sub(r"\d{1,2}(?:[:点时]\d{0,2}分?)", "", stripped)
    classifier = HybridIntentClassifier()
    intent = classifier.classify(stripped)
    if intent.name == "automation":
        intent = classifier.classify(re.sub(r"起床自动", "起床", stripped))
    commands = commands_for_intent(intent, stripped)
    if not commands:
        return None
    return Automation(
        automation_id=uuid.uuid4().hex[:12],
        title=f"{hour:02d}:{minute:02d} · {intent.name}",
        schedule=schedule,
        hour=hour,
        minute=minute,
        source_text=text,
        commands=tuple(commands),
    )


class AutomationStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS automations (
                    automation_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    schedule TEXT NOT NULL,
                    hour INTEGER NOT NULL,
                    minute INTEGER NOT NULL,
                    source_text TEXT NOT NULL,
                    commands_json TEXT NOT NULL,
                    enabled INTEGER NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )

    def add(self, automation: Automation) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO automations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    automation.automation_id,
                    automation.title,
                    automation.schedule,
                    automation.hour,
                    automation.minute,
                    automation.source_text,
                    json.dumps(
                        [asdict(command) for command in automation.commands], ensure_ascii=False
                    ),
                    int(automation.enabled),
                    datetime.now().isoformat(timespec="seconds"),
                ),
            )

    def list(self) -> list[Automation]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM automations ORDER BY hour, minute, created_at"
            ).fetchall()
        return [
            Automation(
                automation_id=row["automation_id"],
                title=row["title"],
                schedule=row["schedule"],
                hour=row["hour"],
                minute=row["minute"],
                source_text=row["source_text"],
                commands=tuple(Command(**command) for command in json.loads(row["commands_json"])),
                enabled=bool(row["enabled"]),
            )
            for row in rows
        ]

    def delete(self, automation_id: str) -> None:
        with self._connect() as connection:
            connection.execute("DELETE FROM automations WHERE automation_id = ?", (automation_id,))
