from collections.abc import Generator

from fastapi import Depends

from implementation.in_memory_user_repository import InMemoryUserRepository
from interface.repository import UserRepository
from use_case.service import UserService

_repo = InMemoryUserRepository()


def get_user_repository() -> Generator[UserRepository, None, None]:
    yield _repo


def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repo=repo)
