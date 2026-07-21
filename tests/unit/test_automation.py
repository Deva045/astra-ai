"""
Unit tests for ai.automation.
"""

from ai.automation import Automation


def test_automation_defaults() -> None:
    automation = Automation(
        automation_id="auto-1",
        name="Backup",
    )

    assert automation.automation_id == "auto-1"
    assert automation.name == "Backup"
    assert automation.description == ""
    assert automation.enabled is True
    assert automation.metadata == {}
    assert automation.created_at is not None


def test_enable_disable() -> None:
    automation = Automation(
        automation_id="auto-1",
        name="Backup",
    )

    automation.disable()
    assert automation.enabled is False

    automation.enable()
    assert automation.enabled is True


def test_metadata() -> None:
    automation = Automation(
        automation_id="auto-1",
        name="Backup",
    )

    automation.update_metadata("interval", "daily")
    automation.update_metadata("priority", 1)

    assert automation.get_metadata("interval") == "daily"
    assert automation.get_metadata("priority") == 1
    assert automation.get_metadata("missing") is None
    assert automation.get_metadata("missing", "default") == "default"
