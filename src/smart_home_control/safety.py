"""Deterministic safety interlocks for every candidate command."""

from __future__ import annotations

from .catalog import get_device
from .domain import Command, SafetyFinding

HIGH_RISK_ACTIONS = {("security.front_door", "unlock")}
HIGH_RISK_INTENTS = {"leave_home_mode"}
HEALTH_CUES = ("感冒", "发烧", "胸闷", "呼吸困难", "婴儿", "老人")


def validate_commands(
    commands: list[Command], *, intent: str, original_text: str
) -> tuple[list[SafetyFinding], str]:
    findings: list[SafetyFinding] = []
    risk = "low"
    if not commands:
        findings.append(SafetyFinding("EMPTY_PLAN", "未生成可执行动作。", "error"))

    for index, command in enumerate(commands):
        device = get_device(command.device_id)
        if device is None:
            findings.append(
                SafetyFinding(
                    "UNKNOWN_DEVICE", f"设备 {command.device_id} 不在白名单中。", "error", index
                )
            )
            continue
        if command.action not in device.capabilities:
            findings.append(
                SafetyFinding(
                    "UNSUPPORTED_ACTION",
                    f"{device.name} 不支持动作 {command.action}。",
                    "error",
                    index,
                )
            )
        for rule in device.parameter_rules:
            if rule.name not in command.parameters:
                continue
            value = command.parameters[rule.name]
            if not isinstance(value, (int, float)) or not rule.minimum <= value <= rule.maximum:
                findings.append(
                    SafetyFinding(
                        "PARAMETER_OUT_OF_RANGE",
                        f"{device.name} 的 {rule.name} 必须在 {rule.minimum:g}-{rule.maximum:g}{rule.unit}。",
                        "error",
                        index,
                    )
                )
        if (command.device_id, command.action) in HIGH_RISK_ACTIONS:
            risk = "high"
            findings.append(
                SafetyFinding(
                    "CONFIRM_UNLOCK", "门锁解锁属于高风险操作，必须二次确认。", "warning", index
                )
            )

    if intent in HIGH_RISK_INTENTS:
        risk = "high"
        findings.append(
            SafetyFinding("CONFIRM_SCENE", "批量离家场景会控制多个设备，必须二次确认。", "warning")
        )
    if any(cue in original_text for cue in HEALTH_CUES):
        risk = "high"
        findings.append(
            SafetyFinding(
                "HEALTH_CONTEXT", "检测到健康相关表达，设备动作不得替代医疗判断。", "warning"
            )
        )
    if risk != "high" and len(commands) >= 4:
        risk = "medium"
        findings.append(SafetyFinding("BATCH_OPERATION", "该场景包含多个设备动作。", "info"))
    return findings, risk


def has_blocking_error(findings: list[SafetyFinding]) -> bool:
    return any(finding.severity == "error" for finding in findings)


def requires_confirmation(findings: list[SafetyFinding]) -> bool:
    return any(
        finding.code.startswith("CONFIRM_") or finding.code == "HEALTH_CONTEXT"
        for finding in findings
    )
