from datetime import datetime, timedelta, timezone
import os

import jwt
from dotenv import load_dotenv

load_dotenv(override=False)

SECRET_JWT_KEY = os.getenv("SECRET_JWT_KEY")
JWT_ALGO = os.getenv("JWT_ALGO")

if not SECRET_JWT_KEY:
    raise RuntimeError(
        "Missing SECRET_JWT_KEY. Put it into auth_service/.env_example or pass via docker-compose env_file."
    )
if not JWT_ALGO:
    raise RuntimeError("Missing JWT_ALGO. Put it into auth_service/.env_example or pass via docker-compose env_file.")

def encode_token(payload: dict, expires_minutes: int) -> str:
    data = payload.copy()
    data["exp"] = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    return jwt.encode(data, SECRET_JWT_KEY, algorithm=JWT_ALGO)

def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_JWT_KEY, algorithms=[JWT_ALGO])
