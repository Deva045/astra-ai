"""
Agent manager for Astra AI.
"""

from __future__ import annotations

from ai.agent import Agent


class AgentManager:
    """Manages registered agents."""

    def __init__(self) -> None:
        self._agents: dict[str, Agent] = {}

    def register(self, agent: Agent) -> None:
        """Register an agent."""
        self._agents[agent.agent_id] = agent

    def unregister(self, agent_id: str) -> bool:
        """Remove an agent by ID."""
        return self._agents.pop(agent_id, None) is not None

    def get(self, agent_id: str) -> Agent | None:
        """Return an agent by ID."""
        return self._agents.get(agent_id)

    def all_agents(self) -> list[Agent]:
        """Return all registered agents."""
        return list(self._agents.values())

    def enabled_agents(self) -> list[Agent]:
        """Return all enabled agents."""
        return [agent for agent in self._agents.values() if agent.enabled]

    def clear(self) -> None:
        """Remove all registered agents."""
        self._agents.clear()

    @property
    def count(self) -> int:
        """Return the number of registered agents."""
        return len(self._agents)
