from collections.abc import Generator

from fastapi import Depends

from implementation.in_memory_auth_repository import InMemoryAuthRepository
from interface.repository import AuthRepository
from use_case.service import AuthService

_repo = InMemoryAuthRepository()


def get_auth_repository() -> Generator[AuthRepository, None, None]:
    yield _repo


def get_auth_service(repo: AuthRepository = Depends(get_auth_repository)) -> AuthService:
    return AuthService(repo=repo)
