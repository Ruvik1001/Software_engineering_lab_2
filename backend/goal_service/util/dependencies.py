"""FastAPI dependency providers for goal service."""

from collections.abc import Generator

from fastapi import Depends, Header, HTTPException

from implementation.in_memory_goal_repository import InMemoryGoalRepository
from interface.repository import GoalRepository
from use_case.service import GoalService

_repo = InMemoryGoalRepository()


def get_goal_repository() -> Generator[GoalRepository, None, None]:
    """Provide goal repository instance."""
    yield _repo


def get_goal_service(repo: GoalRepository = Depends(get_goal_repository)) -> GoalService:
    """Provide goal service instance."""
    return GoalService(repo=repo)


def get_owner_id(x_user_id: int | None = Header(default=None, alias="X-User-Id")) -> int:
    """Extract owner id from X-User-Id header."""

    if x_user_id is None:
        raise HTTPException(status_code=401, detail="missing X-User-Id")
    return int(x_user_id)
