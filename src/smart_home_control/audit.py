"""Append-only JSONL audit trail."""

from __future__ import annotations

import json
from pathlib import Path

from .domain import ControlDecision


class AuditLogger:
    def __init__(self, path: str | Path | None = None) -> None:
        self.path = Path(path) if path else None

    def write(self, decision: ControlDecision) -> None:
        if self.path is None:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(decision.to_dict(), ensure_ascii=False) + "\n")
