from interface.repository import UserRepository


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    def create_user(self, data: dict) -> dict:
        return self._repo.create(**data).__dict__

    def get_by_login(self, login: str) -> dict | None:
        user = self._repo.by_login(login)
        return user.__dict__ if user else None

    def search_by_mask(self, mask: str) -> list[dict]:
        return [u.__dict__ for u in self._repo.by_mask(mask)]
