"""In-memory goal repository implementation."""

from model.goal import Goal


class InMemoryGoalRepository:
    """Stores goals in memory."""

    def __init__(self) -> None:
        """Initialize repository state."""
        self._seq = 1
        self._goals: dict[int, Goal] = {}

    def create(self, title: str, owner_id: int) -> Goal:
        """Create and store a new goal."""
        goal = Goal(id=self._seq, title=title, owner_id=owner_id)
        self._goals[self._seq] = goal
        self._seq += 1
        return goal

    def list_all(self, owner_id: int) -> list[Goal]:
        """List all stored goals for owner."""
        return [g for g in self._goals.values() if g.owner_id == owner_id]
