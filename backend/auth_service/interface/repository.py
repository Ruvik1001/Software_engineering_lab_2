from typing import Protocol

from model.user import AuthUser


class AuthRepository(Protocol):
    def create_user(
        self,
        login: str,
        password: str,
        first_name: str,
        last_name: str,
    ) -> AuthUser: ...

    def get_user(self, login: str) -> AuthUser | None: ...
