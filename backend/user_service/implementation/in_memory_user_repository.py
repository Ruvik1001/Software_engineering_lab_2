from model.user import User


class InMemoryUserRepository:
    def __init__(self) -> None:
        self._seq = 1
        self._users: dict[int, User] = {}

    def create(self, login: str, first_name: str, last_name: str) -> User:
        if any(u.login == login for u in self._users.values()):
            raise ValueError("login already exists")
        user = User(id=self._seq, login=login, first_name=first_name, last_name=last_name)
        self._users[user.id] = user
        self._seq += 1
        return user

    def by_login(self, login: str) -> User | None:
        return next((u for u in self._users.values() if u.login == login), None)

    def by_mask(self, mask: str) -> list[User]:
        m = mask.lower()
        return [u for u in self._users.values() if m in f"{u.first_name} {u.last_name}".lower()]

