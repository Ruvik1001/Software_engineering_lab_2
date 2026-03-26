"""Task repository interface."""

from typing import Protocol

from model.task import Task


class TaskRepository(Protocol):
    """Abstract storage for tasks."""

    def create(self, goal_id: int, title: str, owner_id: int, status: str = "new") -> Task:
        """Create and store a new task."""
        raise NotImplementedError

    def by_goal(self, goal_id: int, owner_id: int) -> list[Task]:
        """List tasks for goal and owner."""
        raise NotImplementedError

    def set_status(self, task_id: int, owner_id: int, status: str) -> Task | None:
        """Update task status and return task if found."""
        raise NotImplementedError
