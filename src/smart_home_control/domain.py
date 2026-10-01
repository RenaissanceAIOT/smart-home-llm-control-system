"""Domain models shared by parsers, safety policy, execution, and UI."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal

RiskLevel = Literal["low", "medium", "high"]
DecisionStatus = Literal["executed", "confirmation_required", "rejected", "no_match", "planned"]


@dataclass(frozen=True, slots=True)
class ParameterRule:
    name: str
    minimum: float
    maximum: float
    unit: str


@dataclass(frozen=True, slots=True)
class DeviceSpec:
    device_id: str
    name: str
    room: str
    category: str
    capabilities: tuple[str, ...]
    parameter_rules: tuple[ParameterRule, ...] = ()
    aliases: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Command:
    device_id: str
    action: str
    parameters: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class SafetyFinding:
    code: str
    message: str
    severity: Literal["info", "warning", "error"]
    command_index: int | None = None


@dataclass(slots=True)
class ControlDecision:
    request_id: str
    text: str
    normalized_text: str
    intent: str
    intent_source: str
    confidence: float
    commands: list[Command]
    findings: list[SafetyFinding]
    risk_level: RiskLevel
    status: DecisionStatus
    message: str
    executed_commands: list[Command] = field(default_factory=list)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds")
    )

    @property
    def needs_confirmation(self) -> bool:
        return self.status == "confirmation_required"

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["needs_confirmation"] = self.needs_confirmation
        return data


@dataclass(frozen=True, slots=True)
class IntentResult:
    name: str
    confidence: float
    source: str
    slots: dict[str, Any] = field(default_factory=dict)
