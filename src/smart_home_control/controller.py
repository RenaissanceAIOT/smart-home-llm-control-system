"""End-to-end orchestration for classify -> plan -> interlock -> execute."""

from __future__ import annotations

import uuid

from .audit import AuditLogger
from .domain import ControlDecision
from .executor import SimulatedExecutor
from .intents import HybridIntentClassifier, LLMIntentClassifier, normalize_text
from .planner import commands_for_intent
from .safety import has_blocking_error, requires_confirmation, validate_commands


class SmartHomeController:
    def __init__(
        self,
        *,
        classifier: HybridIntentClassifier | None = None,
        executor: SimulatedExecutor | None = None,
        audit_logger: AuditLogger | None = None,
        enable_llm_from_env: bool = False,
    ) -> None:
        llm = LLMIntentClassifier.from_env() if enable_llm_from_env else None
        self.classifier = classifier or HybridIntentClassifier(llm)
        self.executor = executor or SimulatedExecutor()
        self.audit_logger = audit_logger or AuditLogger()

    def process(self, text: str, *, confirmed: bool = False) -> ControlDecision:
        request_id = uuid.uuid4().hex[:12]
        normalized = normalize_text(text)
        if not normalized:
            decision = ControlDecision(
                request_id,
                text,
                normalized,
                "unknown",
                "input",
                0.0,
                [],
                [],
                "low",
                "no_match",
                "请输入一条智能家居指令。",
            )
            self.audit_logger.write(decision)
            return decision

        intent = self.classifier.classify(normalized)
        if intent.name == "automation":
            decision = ControlDecision(
                request_id,
                text,
                normalized,
                intent.name,
                intent.source,
                intent.confidence,
                [],
                [],
                "low",
                "planned",
                "已识别为定时自动化，请在“自动化”页保存计划。",
            )
            self.audit_logger.write(decision)
            return decision

        commands = commands_for_intent(intent, normalized)
        findings, risk = validate_commands(commands, intent=intent.name, original_text=normalized)
        if intent.name == "unknown":
            status = "no_match"
            message = "无法可靠判断意图，未生成任何设备动作。请补充房间、设备或期望状态。"
        elif has_blocking_error(findings):
            status = "rejected"
            message = "安全联锁拒绝了该计划，请检查设备、动作或参数。"
        elif requires_confirmation(findings) and not confirmed:
            status = "confirmation_required"
            message = "计划已通过白名单检查，但包含高风险动作，等待二次确认。"
        else:
            status = "executed"
            for command in commands:
                self.executor.execute(command)
            message = f"已安全执行 {len(commands)} 个模拟设备动作。"

        decision = ControlDecision(
            request_id=request_id,
            text=text,
            normalized_text=normalized,
            intent=intent.name,
            intent_source=intent.source,
            confidence=intent.confidence,
            commands=commands,
            findings=findings,
            risk_level=risk,
            status=status,
            message=message,
            executed_commands=commands if status == "executed" else [],
        )
        self.audit_logger.write(decision)
        return decision
