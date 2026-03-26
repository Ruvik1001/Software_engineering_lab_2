from typing import Protocol

from model.goal import Goal


class GoalRepository(Protocol):
    def create(self, title: str, owner_id: int) -> Goal: ...

    def list_all(self, owner_id: int) -> list[Goal]: ...
