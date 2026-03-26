from interface.repository import TaskRepository


class TaskService:
    def __init__(self, repo: TaskRepository) -> None:
        self._repo = repo

    def create_task(self, data: dict, owner_id: int) -> dict:
        task = self._repo.create(
            goal_id=data["goal_id"],
            title=data["title"],
            owner_id=owner_id,
            status=data.get("status", "new"),
        )
        return task.__dict__

    def get_tasks(self, goal_id: int, owner_id: int) -> list[dict]:
        return [t.__dict__ for t in self._repo.by_goal(goal_id, owner_id)]

    def update_status(self, task_id: int, owner_id: int, status: str) -> dict | None:
        task = self._repo.set_status(task_id, owner_id, status)
        return task.__dict__ if task else None
