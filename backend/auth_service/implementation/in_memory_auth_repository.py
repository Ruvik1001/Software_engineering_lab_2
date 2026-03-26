"""In-memory auth repository implementation."""

from model.user import AuthUser


class InMemoryAuthRepository:
    """Stores auth users in memory."""

    def __init__(self) -> None:
        """Initialize repository state."""
        self._seq = 1
        self._users: dict[str, AuthUser] = {}

    def create_user(self, login: str, password: str, first_name: str, last_name: str) -> AuthUser:
        """Create new user credentials, ensuring unique login."""
        if login in self._users:
            raise ValueError("login already exists")
        user = AuthUser(
            id=self._seq,
            login=login,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        self._users[login] = user
        self._seq += 1
        return user

    def get_user(self, login: str) -> AuthUser | None:
        """Return stored user by login."""
        return self._users.get(login)
