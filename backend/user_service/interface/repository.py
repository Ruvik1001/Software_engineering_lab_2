"""User repository interface."""

from typing import Protocol

from model.user import User


class UserRepository(Protocol):
    """Abstract storage for users."""

    def create(self, login: str, first_name: str, last_name: str) -> User:
        """Create and store a new user."""
        raise NotImplementedError

    def by_login(self, login: str) -> User | None:
        """Return user by login if present."""
        raise NotImplementedError

    def by_mask(self, mask: str) -> list[User]:
        """Return list of users matching name mask."""
        raise NotImplementedError
