from interface.repository import GoalRepository


class GoalService:
    def __init__(self, repo: GoalRepository) -> None:
        self._repo = repo

    def create_goal(self, title: str, owner_id: int) -> dict:
        return self._repo.create(title=title, owner_id=owner_id).__dict__

    def list_goals(self, owner_id: int) -> list[dict]:
        return [g.__dict__ for g in self._repo.list_all(owner_id)]
