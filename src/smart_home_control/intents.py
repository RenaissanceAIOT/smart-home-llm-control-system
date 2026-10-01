"""Intent recognition with deterministic rules and an optional constrained LLM."""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass

from .catalog import find_devices
from .domain import IntentResult

KNOWN_INTENTS = (
    "explicit_control",
    "cool_down",
    "warm_up",
    "bath_preparation",
    "sleep_mode",
    "wake_up_mode",
    "leave_home_mode",
    "humidify",
    "purify_air",
    "ventilate",
    "brighten",
    "cooking_mode",
    "cleaning_mode",
    "relax_mode",
    "unlock_door",
    "automation",
    "unknown",
)


def normalize_text(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[，。！？；、,.!?;]", " ", text)
    return re.sub(r"\s+", " ", text)


def _has_any(text: str, phrases: tuple[str, ...]) -> bool:
    return any(phrase in text for phrase in phrases)


class RuleIntentClassifier:
    """High precision local classifier used before any network call."""

    def classify(self, text: str) -> IntentResult:
        normalized = normalize_text(text)
        if re.search(r"(每天|每晚|每周|工作日|周末|定时|自动).{0,14}(\d{1,2})[:点时]", normalized):
            return IntentResult("automation", 0.98, "rule:automation")
        if _has_any(normalized, ("开锁", "打开门锁", "把门打开", "解锁")):
            return IntentResult("unlock_door", 0.99, "rule:high-risk")
        if find_devices(normalized):
            return IntentResult("explicit_control", 0.98, "rule:device-alias")
        if _has_any(normalized, ("离家", "出门了", "没人了", "出门上班")):
            return IntentResult("leave_home_mode", 0.95, "rule:scene")
        if _has_any(normalized, ("起床", "早安", "该醒了", "天亮了", "新的一天")):
            return IntentResult("wake_up_mode", 0.94, "rule:scene")
        if _has_any(normalized, ("睡觉", "晚安", "准备休息", "洗漱睡觉")):
            return IntentResult("sleep_mode", 0.94, "rule:scene")
        if _has_any(normalized, ("洗澡", "热水澡", "沐浴", "冲个澡")):
            return IntentResult("bath_preparation", 0.94, "rule:scene")
        if _has_any(normalized, ("太热", "好热", "闷热", "凉快点", "凉快一点", "降降温")):
            return IntentResult("cool_down", 0.92, "rule:sensation")
        if _has_any(normalized, ("太冷", "好冷", "发冷", "冷飕飕", "暖和点", "暖和一点", "冻死")):
            return IntentResult("warm_up", 0.92, "rule:sensation")
        if _has_any(normalized, ("太干", "空气干", "嗓子干", "嗓子有点干", "加点湿度")):
            return IntentResult("humidify", 0.91, "rule:sensation")
        if _has_any(normalized, ("空气不好", "有异味", "空气浑浊", "净化空气", "干净空气")):
            return IntentResult("purify_air", 0.91, "rule:sensation")
        if _has_any(normalized, ("屋里闷", "透透气", "通通风", "空气不流通")):
            return IntentResult("ventilate", 0.90, "rule:sensation")
        if _has_any(normalized, ("太暗", "有点暗", "看不清", "亮一点", "屋里黑", "黑乎乎")):
            return IntentResult("brighten", 0.90, "rule:sensation")
        if _has_any(normalized, ("开始做饭", "准备做饭", "开始炒菜", "炒菜了", "晚餐时间")):
            return IntentResult("cooking_mode", 0.91, "rule:scene")
        if _has_any(normalized, ("该打扫了", "地上有灰", "清扫一下")):
            return IntentResult("cleaning_mode", 0.90, "rule:scene")
        if _has_any(normalized, ("看电影", "放松一下", "休息一会", "追剧", "追个剧")):
            return IntentResult("relax_mode", 0.86, "rule:scene")
        return IntentResult("unknown", 0.0, "rule:no-match")


@dataclass(slots=True)
class LLMIntentClassifier:
    """OpenAI-compatible classifier that may output only a known intent label."""

    api_key: str
    model: str = "gpt-4.1-mini"
    base_url: str = "https://api.openai.com/v1"
    timeout_seconds: float = 12.0

    @classmethod
    def from_env(cls) -> LLMIntentClassifier | None:
        key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not key:
            return None
        return cls(
            api_key=key,
            model=os.getenv("LLM_MODEL", "gpt-4.1-mini"),
            base_url=os.getenv("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/"),
        )

    def classify(self, text: str) -> IntentResult:
        labels = ", ".join(intent for intent in KNOWN_INTENTS if intent != "unknown")
        prompt = (
            "你是智能家居意图分类器。只判断意图，不得生成设备、动作或参数。"
            f"可选标签：{labels}, unknown。"
            '严格输出 JSON：{"intent":"标签"}。用户输入：' + text
        )
        payload = json.dumps(
            {
                "model": self.model,
                "temperature": 0,
                "messages": [{"role": "user", "content": prompt}],
                "response_format": {"type": "json_object"},
            }
        ).encode("utf-8")
        request = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                body = json.loads(response.read().decode("utf-8"))
            content = body["choices"][0]["message"]["content"]
            intent = json.loads(content).get("intent", "unknown")
        except (urllib.error.URLError, TimeoutError, KeyError, ValueError, json.JSONDecodeError):
            return IntentResult("unknown", 0.0, "llm:error")
        if intent not in KNOWN_INTENTS:
            return IntentResult("unknown", 0.0, "llm:invalid-label")
        return IntentResult(intent, 0.78 if intent != "unknown" else 0.0, f"llm:{self.model}")


class HybridIntentClassifier:
    """Rules first; constrained LLM only for otherwise unknown language."""

    def __init__(self, llm: LLMIntentClassifier | None = None) -> None:
        self.rules = RuleIntentClassifier()
        self.llm = llm

    def classify(self, text: str) -> IntentResult:
        result = self.rules.classify(text)
        if result.name != "unknown" or self.llm is None:
            return result
        llm_result = self.llm.classify(text)
        if llm_result.name == "unknown":
            return IntentResult("unknown", 0.0, f"{llm_result.source};conservative-fallback")
        return llm_result
