"""
Unit tests for ai.automation_manager.
"""

from ai.automation import Automation
from ai.automation_manager import AutomationManager


def test_register_and_get() -> None:
    manager = AutomationManager()

    automation = Automation(
        automation_id="auto-1",
        name="Backup",
    )

    manager.register(automation)

    assert manager.count == 1
    assert manager.get("auto-1") is automation
    assert manager.get("missing") is None


def test_unregister() -> None:
    manager = AutomationManager()

    automation = Automation(
        automation_id="auto-1",
        name="Backup",
    )

    manager.register(automation)

    assert manager.unregister("auto-1") is True
    assert manager.count == 0
    assert manager.unregister("auto-1") is False


def test_all_automations() -> None:
    manager = AutomationManager()

    a1 = Automation(automation_id="1", name="One")
    a2 = Automation(automation_id="2", name="Two")

    manager.register(a1)
    manager.register(a2)

    automations = manager.all_automations()

    assert len(automations) == 2
    assert a1 in automations
    assert a2 in automations


def test_enabled_automations() -> None:
    manager = AutomationManager()

    enabled = Automation(automation_id="1", name="Enabled")
    disabled = Automation(automation_id="2", name="Disabled")

    disabled.disable()

    manager.register(enabled)
    manager.register(disabled)

    automations = manager.enabled_automations()

    assert len(automations) == 1
    assert automations[0] is enabled


def test_clear() -> None:
    manager = AutomationManager()

    manager.register(Automation(automation_id="1", name="One"))
    manager.register(Automation(automation_id="2", name="Two"))

    assert manager.count == 2

    manager.clear()

    assert manager.count == 0
    assert manager.all_automations() == []
