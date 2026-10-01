"""In-memory simulated device executor with idempotent state transitions."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from .catalog import DEVICE_CATALOG
from .domain import Command


class SimulatedExecutor:
    def __init__(self) -> None:
        self._state: dict[str, dict[str, Any]] = {
            device.device_id: {"power": "off", "last_action": None} for device in DEVICE_CATALOG
        }
        self._state["security.front_door"]["locked"] = True
        self._state["security.smoke_alarm"]["power"] = "on"

    def execute(self, command: Command) -> dict[str, Any]:
        state = self._state[command.device_id]
        action = command.action
        if action == "turn_on":
            state["power"] = "on"
        elif action == "turn_off":
            state["power"] = "off"
        elif action == "lock":
            state["locked"] = True
        elif action == "unlock":
            state["locked"] = False
        elif action in {"open", "close"}:
            state["position"] = 100 if action == "open" else 0
        elif action.startswith("set_"):
            state.update(command.parameters)
            state["power"] = "on"
        elif action in {"test", "mute"}:
            state["alarm_state"] = action
        state["last_action"] = action
        return deepcopy(state)

    def snapshot(self) -> dict[str, dict[str, Any]]:
        return deepcopy(self._state)
