from interface.repository import AuthRepository
from model.user import AuthUser
from util.security import decode_token, encode_token


class AuthService:
    def __init__(self, repo: AuthRepository) -> None:
        self._repo = repo

    def register(self, data: dict) -> dict:
        created = self._repo.create_user(
            login=data["login"],
            password=data["password"],
            first_name=data["first_name"],
            last_name=data["last_name"],
        )
        return {
            "user_id": created.id,
            "login": created.login,
            "first_name": created.first_name,
            "last_name": created.last_name,
        }

    def login(self, login_value: str, password: str) -> dict:
        user = self._repo.get_user(login_value)
        if not user or user.password != password:
            raise ValueError("invalid credentials")
        access_token = encode_token({"sub": str(user.id)}, expires_minutes=30)
        refresh_token = encode_token({"sub": str(user.id), "kind": "refresh"}, expires_minutes=60 * 24)
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

    def refresh(self, token: str) -> dict:
        payload = decode_token(token)
        if payload.get("kind") != "refresh":
            raise ValueError("invalid refresh token")
        access_token = encode_token({"sub": str(payload["sub"])}, expires_minutes=30)
        return {"access_token": access_token, "token_type": "bearer"}

    def validate(self, token: str) -> dict:
        payload = decode_token(token)
        return {"user_id": int(payload.get("sub"))}
