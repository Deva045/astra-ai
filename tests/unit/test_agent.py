"""
Unit tests for ai.agent.
"""

from ai.agent import Agent


def test_agent_defaults() -> None:
    agent = Agent(
        agent_id="agent-1",
        name="Assistant",
    )

    assert agent.agent_id == "agent-1"
    assert agent.name == "Assistant"
    assert agent.description == ""
    assert agent.enabled is True
    assert agent.metadata == {}
    assert agent.created_at is not None


def test_enable_disable() -> None:
    agent = Agent(
        agent_id="agent-1",
        name="Assistant",
    )

    agent.disable()
    assert agent.enabled is False

    agent.enable()
    assert agent.enabled is True


def test_metadata() -> None:
    agent = Agent(
        agent_id="agent-1",
        name="Assistant",
    )

    agent.update_metadata("role", "planner")
    agent.update_metadata("priority", 10)

    assert agent.get_metadata("role") == "planner"
    assert agent.get_metadata("priority") == 10
    assert agent.get_metadata("missing") is None
    assert agent.get_metadata("missing", "default") == "default"
