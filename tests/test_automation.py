from smart_home_control.automation import AutomationStore, parse_automation


def test_parse_and_persist_daily_automation(tmp_path) -> None:
    automation = parse_automation("每天早上6点起床，自动打开卧室窗帘")
    assert automation is not None
    assert (automation.hour, automation.minute) == (6, 0)
    assert automation.schedule == "daily"
    assert automation.commands[0].device_id == "curtain.bedroom"

    store = AutomationStore(tmp_path / "automations.db")
    store.add(automation)
    loaded = store.list()
    assert loaded == [automation]
    store.delete(automation.automation_id)
    assert store.list() == []


def test_invalid_time_does_not_create_automation() -> None:
    assert parse_automation("每天30点打开客厅灯") is None
