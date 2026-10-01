"""Device allowlist and capability catalog.

The 47-device inventory mirrors the scale described by the source report while
remaining entirely simulated. Integrations should map their real entity IDs to
these stable logical IDs instead of allowing model-generated identifiers.
"""

from __future__ import annotations

from .domain import DeviceSpec, ParameterRule

BRIGHTNESS = ParameterRule("brightness", 0, 100, "%")
TEMPERATURE = ParameterRule("temperature", 16, 30, "°C")
WATER_TEMPERATURE = ParameterRule("water_temperature", 35, 55, "°C")
POSITION = ParameterRule("position", 0, 100, "%")
VOLUME = ParameterRule("volume", 0, 100, "%")


def _device(
    device_id: str,
    name: str,
    room: str,
    category: str,
    capabilities: tuple[str, ...],
    *rules: ParameterRule,
    aliases: tuple[str, ...] = (),
) -> DeviceSpec:
    return DeviceSpec(device_id, name, room, category, capabilities, rules, aliases)


DEVICE_CATALOG: tuple[DeviceSpec, ...] = (
    _device(
        "light.living_main",
        "客厅主灯",
        "客厅",
        "lighting",
        ("turn_on", "turn_off", "set_brightness"),
        BRIGHTNESS,
        aliases=("客厅灯",),
    ),
    _device(
        "light.living_ambient",
        "客厅氛围灯",
        "客厅",
        "lighting",
        ("turn_on", "turn_off", "set_brightness"),
        BRIGHTNESS,
    ),
    _device(
        "light.dining",
        "餐厅吊灯",
        "餐厅",
        "lighting",
        ("turn_on", "turn_off", "set_brightness"),
        BRIGHTNESS,
        aliases=("餐厅灯",),
    ),
    _device(
        "light.kitchen",
        "厨房顶灯",
        "厨房",
        "lighting",
        ("turn_on", "turn_off", "set_brightness"),
        BRIGHTNESS,
        aliases=("厨房灯",),
    ),
    _device(
        "light.bedroom_main",
        "主卧顶灯",
        "主卧",
        "lighting",
        ("turn_on", "turn_off", "set_brightness"),
        BRIGHTNESS,
        aliases=("卧室灯", "主卧灯"),
    ),
    _device(
        "light.bedside",
        "主卧床头灯",
        "主卧",
        "lighting",
        ("turn_on", "turn_off", "set_brightness"),
        BRIGHTNESS,
        aliases=("床头灯",),
    ),
    _device(
        "light.bedroom_second",
        "次卧顶灯",
        "次卧",
        "lighting",
        ("turn_on", "turn_off", "set_brightness"),
        BRIGHTNESS,
        aliases=("次卧灯",),
    ),
    _device(
        "light.study",
        "书房灯",
        "书房",
        "lighting",
        ("turn_on", "turn_off", "set_brightness"),
        BRIGHTNESS,
    ),
    _device(
        "light.bathroom",
        "卫生间灯",
        "卫生间",
        "lighting",
        ("turn_on", "turn_off", "set_brightness"),
        BRIGHTNESS,
    ),
    _device(
        "light.entry",
        "玄关灯",
        "玄关",
        "lighting",
        ("turn_on", "turn_off", "set_brightness"),
        BRIGHTNESS,
    ),
    _device(
        "light.balcony",
        "阳台灯",
        "阳台",
        "lighting",
        ("turn_on", "turn_off", "set_brightness"),
        BRIGHTNESS,
    ),
    _device(
        "light.hallway",
        "走廊灯",
        "走廊",
        "lighting",
        ("turn_on", "turn_off", "set_brightness"),
        BRIGHTNESS,
    ),
    _device(
        "light.cloakroom",
        "衣帽间灯",
        "衣帽间",
        "lighting",
        ("turn_on", "turn_off", "set_brightness"),
        BRIGHTNESS,
    ),
    _device(
        "light.children",
        "儿童房灯",
        "儿童房",
        "lighting",
        ("turn_on", "turn_off", "set_brightness"),
        BRIGHTNESS,
    ),
    _device(
        "light.garage",
        "车库灯",
        "车库",
        "lighting",
        ("turn_on", "turn_off", "set_brightness"),
        BRIGHTNESS,
    ),
    _device(
        "climate.living_ac",
        "客厅空调",
        "客厅",
        "climate",
        ("turn_on", "turn_off", "set_temperature", "set_mode"),
        TEMPERATURE,
    ),
    _device(
        "climate.bedroom_ac",
        "主卧空调",
        "主卧",
        "climate",
        ("turn_on", "turn_off", "set_temperature", "set_mode"),
        TEMPERATURE,
        aliases=("卧室空调",),
    ),
    _device(
        "climate.second_ac",
        "次卧空调",
        "次卧",
        "climate",
        ("turn_on", "turn_off", "set_temperature", "set_mode"),
        TEMPERATURE,
    ),
    _device(
        "climate.fresh_air", "新风系统", "全屋", "climate", ("turn_on", "turn_off", "set_mode")
    ),
    _device(
        "kitchen_bath.water_heater",
        "卫生间热水器",
        "卫生间",
        "kitchen_bath",
        ("turn_on", "turn_off", "set_water_temperature"),
        WATER_TEMPERATURE,
        aliases=("热水器",),
    ),
    _device(
        "kitchen_bath.range_hood",
        "厨房油烟机",
        "厨房",
        "kitchen_bath",
        ("turn_on", "turn_off", "set_mode"),
        aliases=("油烟机",),
    ),
    _device(
        "kitchen_bath.dishwasher",
        "厨房洗碗机",
        "厨房",
        "kitchen_bath",
        ("turn_on", "turn_off", "set_mode"),
        aliases=("洗碗机",),
    ),
    _device(
        "kitchen_bath.water_purifier",
        "厨房净水器",
        "厨房",
        "kitchen_bath",
        ("turn_on", "turn_off"),
        aliases=("净水器",),
    ),
    _device(
        "kitchen_bath.rice_cooker",
        "电饭煲",
        "厨房",
        "kitchen_bath",
        ("turn_on", "turn_off", "set_mode"),
    ),
    _device(
        "kitchen_bath.oven", "烤箱", "厨房", "kitchen_bath", ("turn_on", "turn_off", "set_mode")
    ),
    _device(
        "kitchen_bath.microwave",
        "微波炉",
        "厨房",
        "kitchen_bath",
        ("turn_on", "turn_off", "set_mode"),
    ),
    _device(
        "kitchen_bath.coffee", "咖啡机", "厨房", "kitchen_bath", ("turn_on", "turn_off", "set_mode")
    ),
    _device(
        "kitchen_bath.bath_heater",
        "浴霸",
        "卫生间",
        "kitchen_bath",
        ("turn_on", "turn_off", "set_mode"),
    ),
    _device("kitchen_bath.water_valve", "厨房水阀", "厨房", "kitchen_bath", ("open", "close")),
    _device(
        "kitchen_bath.exhaust",
        "卫生间排风扇",
        "卫生间",
        "kitchen_bath",
        ("turn_on", "turn_off"),
        aliases=("排风扇",),
    ),
    _device(
        "door_window.living_window",
        "客厅窗",
        "客厅",
        "door_window",
        ("open", "close"),
        aliases=("客厅窗户",),
    ),
    _device(
        "door_window.bedroom_window",
        "主卧窗",
        "主卧",
        "door_window",
        ("open", "close"),
        aliases=("卧室窗", "卧室窗户"),
    ),
    _device("door_window.second_window", "次卧窗", "次卧", "door_window", ("open", "close")),
    _device(
        "door_window.kitchen_window",
        "厨房窗",
        "厨房",
        "door_window",
        ("open", "close"),
        aliases=("厨房窗户",),
    ),
    _device("door_window.balcony_door", "阳台门", "阳台", "door_window", ("open", "close")),
    _device(
        "curtain.living", "客厅窗帘", "客厅", "curtain", ("open", "close", "set_position"), POSITION
    ),
    _device(
        "curtain.bedroom",
        "主卧窗帘",
        "主卧",
        "curtain",
        ("open", "close", "set_position"),
        POSITION,
        aliases=("卧室窗帘",),
    ),
    _device(
        "curtain.second", "次卧窗帘", "次卧", "curtain", ("open", "close", "set_position"), POSITION
    ),
    _device(
        "curtain.study", "书房窗帘", "书房", "curtain", ("open", "close", "set_position"), POSITION
    ),
    _device(
        "appliance.humidifier",
        "客厅加湿器",
        "客厅",
        "appliance",
        ("turn_on", "turn_off", "set_mode"),
        aliases=("加湿器",),
    ),
    _device(
        "appliance.air_purifier",
        "客厅空气净化器",
        "客厅",
        "appliance",
        ("turn_on", "turn_off", "set_mode"),
        aliases=("空气净化器", "净化器"),
    ),
    _device(
        "appliance.robot_vacuum",
        "扫地机器人",
        "全屋",
        "appliance",
        ("turn_on", "turn_off", "set_mode"),
    ),
    _device("appliance.washer", "洗衣机", "阳台", "appliance", ("turn_on", "turn_off", "set_mode")),
    _device(
        "media.television",
        "客厅电视",
        "客厅",
        "media",
        ("turn_on", "turn_off", "set_volume"),
        VOLUME,
        aliases=("电视",),
    ),
    _device(
        "media.speaker",
        "客厅音箱",
        "客厅",
        "media",
        ("turn_on", "turn_off", "set_volume"),
        VOLUME,
        aliases=("音箱",),
    ),
    _device(
        "security.front_door",
        "智能门锁",
        "玄关",
        "security",
        ("lock", "unlock"),
        aliases=("门锁", "大门"),
    ),
    _device(
        "security.smoke_alarm",
        "烟雾报警器",
        "厨房",
        "security",
        ("test", "mute"),
        aliases=("烟感", "烟雾警报器"),
    ),
)

DEVICES_BY_ID = {device.device_id: device for device in DEVICE_CATALOG}
DEVICE_ALIASES = {
    alias: device.device_id for device in DEVICE_CATALOG for alias in (device.name, *device.aliases)
}


def get_device(device_id: str) -> DeviceSpec | None:
    return DEVICES_BY_ID.get(device_id)


def find_devices(text: str) -> list[DeviceSpec]:
    """Return all allowlisted devices explicitly named in *text*, longest alias first."""
    found: list[DeviceSpec] = []
    seen: set[str] = set()
    for alias in sorted(DEVICE_ALIASES, key=len, reverse=True):
        if alias in text:
            device_id = DEVICE_ALIASES[alias]
            if device_id not in seen:
                found.append(DEVICES_BY_ID[device_id])
                seen.add(device_id)
    return found
