"""In-memory user repository implementation."""

from model.user import User


class InMemoryUserRepository:
    """Stores users in memory."""

    def __init__(self) -> None:
        """Initialize repository state."""
        self._seq = 1
        self._users: dict[int, User] = {}

    def create(self, login: str, first_name: str, last_name: str) -> User:
        """Create and store a new user."""
        if any(u.login == login for u in self._users.values()):
            raise ValueError("login already exists")
        user = User(id=self._seq, login=login, first_name=first_name, last_name=last_name)
        self._users[user.id] = user
        self._seq += 1
        return user

    def by_login(self, login: str) -> User | None:
        """Return user by login if present."""
        return next((u for u in self._users.values() if u.login == login), None)

    def by_mask(self, mask: str) -> list[User]:
        """Return users whose first/last name contains mask."""
        m = mask.lower()
        return [u for u in self._users.values() if m in f"{u.first_name} {u.last_name}".lower()]
