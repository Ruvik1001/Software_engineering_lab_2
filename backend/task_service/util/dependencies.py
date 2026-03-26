"""FastAPI dependency providers for task service."""

from collections.abc import Generator

from fastapi import Depends, Header, HTTPException

from implementation.in_memory_task_repository import InMemoryTaskRepository
from interface.repository import TaskRepository
from use_case.service import TaskService

_repo = InMemoryTaskRepository()


def get_task_repository() -> Generator[TaskRepository, None, None]:
    """Provide task repository instance."""
    yield _repo


def get_task_service(repo: TaskRepository = Depends(get_task_repository)) -> TaskService:
    """Provide task service instance."""
    return TaskService(repo=repo)


def get_owner_id(x_user_id: int | None = Header(default=None, alias="X-User-Id")) -> int:
    """Extract owner id from X-User-Id header."""
    if x_user_id is None:
        raise HTTPException(status_code=401, detail="missing X-User-Id")
    return int(x_user_id)
