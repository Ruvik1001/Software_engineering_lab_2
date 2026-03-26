"""Goal repository interface."""

from typing import Protocol

from model.goal import Goal


class GoalRepository(Protocol):
    """Abstract storage for goals."""

    def create(self, title: str, owner_id: int) -> Goal:
        """Create and store a new goal."""
        raise NotImplementedError

    def list_all(self, owner_id: int) -> list[Goal]:
        """List goals for owner."""
        raise NotImplementedError
