"""Auth repository interface."""

from typing import Protocol

from model.user import AuthUser


class AuthRepository(Protocol):
    """Abstract storage for auth users."""

    def create_user(
        self,
        login: str,
        password: str,
        first_name: str,
        last_name: str,
    ) -> AuthUser:
        """Create and store a new auth user."""
        raise NotImplementedError

    def get_user(self, login: str) -> AuthUser | None:
        """Return auth user by login if present."""
        raise NotImplementedError
