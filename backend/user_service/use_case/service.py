"""User service business logic."""

from interface.repository import UserRepository


class UserService:
    """Use-case layer for user operations."""

    def __init__(self, repo: UserRepository) -> None:
        """Create service with provided repository."""
        self._repo = repo

    def create_user(self, data: dict) -> dict:
        """Create a new user and return serializable dict."""
        return self._repo.create(**data).__dict__

    def get_by_login(self, login: str) -> dict | None:
        """Return user dict by login, if exists."""
        user = self._repo.by_login(login)
        return user.__dict__ if user else None

    def search_by_mask(self, mask: str) -> list[dict]:
        """Return list of user dicts matching mask."""
        return [u.__dict__ for u in self._repo.by_mask(mask)]
