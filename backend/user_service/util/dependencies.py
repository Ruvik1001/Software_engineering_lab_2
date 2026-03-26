"""FastAPI dependency providers for user service."""

from collections.abc import Generator

from fastapi import Depends

from implementation.in_memory_user_repository import InMemoryUserRepository
from interface.repository import UserRepository
from use_case.service import UserService

_repo = InMemoryUserRepository()


def get_user_repository() -> Generator[UserRepository, None, None]:
    """Provide user repository instance."""
    yield _repo


def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    """Provide user service instance."""
    return UserService(repo=repo)
