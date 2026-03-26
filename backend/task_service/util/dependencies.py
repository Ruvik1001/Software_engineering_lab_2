from collections.abc import Generator

from fastapi import Depends, Header, HTTPException

from implementation.in_memory_task_repository import InMemoryTaskRepository
from interface.repository import TaskRepository
from use_case.service import TaskService

_repo = InMemoryTaskRepository()


def get_task_repository() -> Generator[TaskRepository, None, None]:
    yield _repo


def get_task_service(repo: TaskRepository = Depends(get_task_repository)) -> TaskService:
    return TaskService(repo=repo)


def get_owner_id(x_user_id: int | None = Header(default=None, alias="X-User-Id")) -> int:
    if x_user_id is None:
        raise HTTPException(status_code=401, detail="missing X-User-Id")
    return int(x_user_id)
