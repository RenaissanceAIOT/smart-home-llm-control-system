from smart_home_control.controller import SmartHomeController
from smart_home_control.domain import Command, IntentResult
from smart_home_control.intents import HybridIntentClassifier
from smart_home_control.safety import validate_commands


def test_explicit_parameter_command_executes() -> None:
    controller = SmartHomeController()
    decision = controller.process("把客厅灯亮度调到50%")
    assert decision.status == "executed"
    assert decision.intent == "explicit_control"
    assert decision.commands == [Command("light.living_main", "set_brightness", {"brightness": 50})]
    assert controller.executor.snapshot()["light.living_main"]["brightness"] == 50


def test_implicit_temperature_command_uses_fixed_rule() -> None:
    decision = SmartHomeController().process("今天好热，我要去卧室休息一会")
    assert decision.status == "executed"
    assert decision.intent == "cool_down"
    assert decision.commands[0].device_id == "climate.bedroom_ac"
    assert decision.commands[0].parameters == {"temperature": 24}


def test_unlock_never_executes_without_confirmation() -> None:
    controller = SmartHomeController()
    pending = controller.process("打开门锁")
    assert pending.status == "confirmation_required"
    assert controller.executor.snapshot()["security.front_door"]["locked"] is True
    executed = controller.process("打开门锁", confirmed=True)
    assert executed.status == "executed"
    assert controller.executor.snapshot()["security.front_door"]["locked"] is False


def test_out_of_range_parameter_is_rejected() -> None:
    decision = SmartHomeController().process("把卧室空调温度调到35度")
    assert decision.status == "rejected"
    assert any(finding.code == "PARAMETER_OUT_OF_RANGE" for finding in decision.findings)


def test_unknown_language_fails_closed() -> None:
    decision = SmartHomeController().process("随便弄得舒服一点")
    assert decision.status == "no_match"
    assert decision.executed_commands == []


def test_unknown_device_is_detected_as_hallucination() -> None:
    findings, risk = validate_commands(
        [Command("appliance.time_machine", "turn_on")],
        intent="explicit_control",
        original_text="打开时间机器",
    )
    assert risk == "low"
    assert findings[0].code == "UNKNOWN_DEVICE"


def test_llm_label_cannot_directly_inject_commands() -> None:
    class FakeLLM:
        def classify(self, text: str) -> IntentResult:
            return IntentResult("cool_down", 0.8, "llm:test")

    classifier = HybridIntentClassifier(FakeLLM())
    controller = SmartHomeController(classifier=classifier)
    decision = controller.process("给我安排一个舒服的环境")
    assert decision.commands == [
        Command("climate.living_ac", "set_temperature", {"temperature": 24})
    ]
