from typing import Protocol

from model.task import Task


class TaskRepository(Protocol):
    def create(self, goal_id: int, title: str, owner_id: int, status: str = "new") -> Task: ...

    def by_goal(self, goal_id: int, owner_id: int) -> list[Task]: ...

    def set_status(self, task_id: int, owner_id: int, status: str) -> Task | None: ...
