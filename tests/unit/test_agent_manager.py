"""
Unit tests for ai.agent_manager.
"""

from ai.agent import Agent
from ai.agent_manager import AgentManager


def test_register_and_get() -> None:
    manager = AgentManager()

    agent = Agent(
        agent_id="agent-1",
        name="Assistant",
    )

    manager.register(agent)

    assert manager.count == 1
    assert manager.get("agent-1") is agent
    assert manager.get("missing") is None


def test_unregister() -> None:
    manager = AgentManager()

    agent = Agent(
        agent_id="agent-1",
        name="Assistant",
    )

    manager.register(agent)

    assert manager.unregister("agent-1") is True
    assert manager.count == 0
    assert manager.unregister("agent-1") is False


def test_all_agents() -> None:
    manager = AgentManager()

    a1 = Agent(agent_id="1", name="One")
    a2 = Agent(agent_id="2", name="Two")

    manager.register(a1)
    manager.register(a2)

    agents = manager.all_agents()

    assert len(agents) == 2
    assert a1 in agents
    assert a2 in agents


def test_enabled_agents() -> None:
    manager = AgentManager()

    enabled = Agent(agent_id="1", name="Enabled")
    disabled = Agent(agent_id="2", name="Disabled")

    disabled.disable()

    manager.register(enabled)
    manager.register(disabled)

    agents = manager.enabled_agents()

    assert len(agents) == 1
    assert agents[0] is enabled


def test_clear() -> None:
    manager = AgentManager()

    manager.register(Agent(agent_id="1", name="One"))
    manager.register(Agent(agent_id="2", name="Two"))

    assert manager.count == 2

    manager.clear()

    assert manager.count == 0
    assert manager.all_agents() == []
