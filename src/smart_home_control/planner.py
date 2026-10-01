"""Map recognized intents to deterministic, allowlisted commands."""

from __future__ import annotations

import re

from .catalog import DEVICE_CATALOG, find_devices
from .domain import Command, IntentResult

ACTION_TERMS: tuple[tuple[tuple[str, ...], str], ...] = (
    (("关闭", "关掉", "关上", "停掉"), "turn_off"),
    (("打开", "开启", "启动", "开一下"), "turn_on"),
    (("拉开", "展开"), "open"),
    (("合上", "拉上"), "close"),
    (("上锁", "锁门", "锁上"), "lock"),
    (("解锁", "开锁"), "unlock"),
)


def _number(text: str, patterns: tuple[str, ...]) -> int | None:
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return int(match.group(1))
    return None


def _explicit_commands(text: str) -> list[Command]:
    commands: list[Command] = []
    temperature = _number(text, (r"(?:温度|调到|设为|设置到)\s*(\d{1,3})\s*度?",))
    brightness = _number(text, (r"(?:亮度|调到|设为)\s*(\d{1,3})\s*%?",))
    position = _number(text, (r"(?:窗帘|开合度|位置).{0,6}(\d{1,3})\s*%",))
    volume = _number(text, (r"(?:音量|声音).{0,6}(\d{1,3})\s*%?",))

    for device in find_devices(text):
        action: str | None = None
        parameters: dict[str, int | str] = {}
        if temperature is not None and "set_temperature" in device.capabilities:
            action, parameters = "set_temperature", {"temperature": temperature}
        elif temperature is not None and "set_water_temperature" in device.capabilities:
            action, parameters = "set_water_temperature", {"water_temperature": temperature}
        elif brightness is not None and "set_brightness" in device.capabilities:
            action, parameters = "set_brightness", {"brightness": brightness}
        elif position is not None and "set_position" in device.capabilities:
            action, parameters = "set_position", {"position": position}
        elif volume is not None and "set_volume" in device.capabilities:
            action, parameters = "set_volume", {"volume": volume}
        else:
            for terms, candidate in ACTION_TERMS:
                if any(term in text for term in terms):
                    action = candidate
                    break

        if (
            action == "turn_on"
            and "turn_on" not in device.capabilities
            and "open" in device.capabilities
        ):
            action = "open"
        if (
            action == "turn_off"
            and "turn_off" not in device.capabilities
            and "close" in device.capabilities
        ):
            action = "close"
        if action is not None:
            commands.append(Command(device.device_id, action, parameters))
    return commands


def commands_for_intent(intent: IntentResult, text: str) -> list[Command]:
    if intent.name == "explicit_control":
        return _explicit_commands(text)
    if intent.name == "unlock_door":
        return [Command("security.front_door", "unlock")]
    if intent.name == "cool_down":
        room = "climate.bedroom_ac" if "卧室" in text or "休息" in text else "climate.living_ac"
        return [Command(room, "set_temperature", {"temperature": 24})]
    if intent.name == "warm_up":
        room = "climate.bedroom_ac" if "卧室" in text else "climate.living_ac"
        return [Command(room, "set_temperature", {"temperature": 27})]
    if intent.name == "bath_preparation":
        return [
            Command("kitchen_bath.water_heater", "turn_on"),
            Command("light.bathroom", "turn_on"),
            Command("kitchen_bath.bath_heater", "turn_on"),
        ]
    if intent.name == "sleep_mode":
        return [
            Command("light.bedroom_main", "turn_off"),
            Command("light.bedside", "set_brightness", {"brightness": 15}),
            Command("curtain.bedroom", "close"),
            Command("climate.bedroom_ac", "set_temperature", {"temperature": 25}),
        ]
    if intent.name == "wake_up_mode":
        return [
            Command("curtain.bedroom", "open"),
            Command("light.bedroom_main", "set_brightness", {"brightness": 65}),
            Command("climate.bedroom_ac", "set_temperature", {"temperature": 25}),
        ]
    if intent.name == "leave_home_mode":
        commands = [
            Command(d.device_id, "turn_off") for d in DEVICE_CATALOG if "turn_off" in d.capabilities
        ]
        commands += [Command("curtain.living", "close"), Command("security.front_door", "lock")]
        return commands
    if intent.name == "humidify":
        return [Command("appliance.humidifier", "turn_on")]
    if intent.name == "purify_air":
        return [Command("appliance.air_purifier", "turn_on")]
    if intent.name == "ventilate":
        return [
            Command("door_window.living_window", "open"),
            Command("climate.fresh_air", "turn_on"),
        ]
    if intent.name == "brighten":
        return [Command("light.living_main", "set_brightness", {"brightness": 75})]
    if intent.name == "cooking_mode":
        return [
            Command("light.kitchen", "turn_on"),
            Command("kitchen_bath.range_hood", "turn_on"),
        ]
    if intent.name == "cleaning_mode":
        return [Command("appliance.robot_vacuum", "turn_on")]
    if intent.name == "relax_mode":
        return [
            Command("light.living_main", "set_brightness", {"brightness": 25}),
            Command("media.television", "turn_on"),
            Command("curtain.living", "close"),
        ]
    return []
