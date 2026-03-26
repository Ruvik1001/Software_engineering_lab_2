from typing import Protocol

from model.user import User


class UserRepository(Protocol):
    def create(self, login: str, first_name: str, last_name: str) -> User: ...

    def by_login(self, login: str) -> User | None: ...

    def by_mask(self, mask: str) -> list[User]: ...
