"""Goal service business logic."""

from interface.repository import GoalRepository


class GoalService:
    """Use-case layer for goal operations."""

    def __init__(self, repo: GoalRepository) -> None:
        """Create service with provided repository."""
        self._repo = repo

    def create_goal(self, title: str, owner_id: int) -> dict:
        """Create goal and return serializable dict."""
        return self._repo.create(title=title, owner_id=owner_id).__dict__

    def list_goals(self, owner_id: int) -> list[dict]:
        """List all goals for owner and return serializable dicts."""
        return [g.__dict__ for g in self._repo.list_all(owner_id)]
