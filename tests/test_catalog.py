from collections import Counter

from smart_home_control.catalog import DEVICE_CATALOG, find_devices


def test_catalog_contains_47_unique_allowlisted_devices() -> None:
    assert len(DEVICE_CATALOG) == 47
    assert len({device.device_id for device in DEVICE_CATALOG}) == 47


def test_catalog_covers_reported_categories() -> None:
    assert Counter(device.category for device in DEVICE_CATALOG) == {
        "lighting": 15,
        "kitchen_bath": 11,
        "climate": 4,
        "door_window": 5,
        "curtain": 4,
        "appliance": 4,
        "media": 2,
        "security": 2,
    }


def test_alias_resolution_prefers_specific_devices() -> None:
    devices = find_devices("请打开卧室空调和床头灯")
    assert [device.device_id for device in devices] == [
        "climate.bedroom_ac",
        "light.bedside",
    ]
