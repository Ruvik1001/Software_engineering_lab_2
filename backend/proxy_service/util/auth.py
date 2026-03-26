from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import httpx

from util.config import AUTH_URL

bearer_scheme = HTTPBearer(auto_error=False)


def get_token_value(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    # NOTE: HTTPBearer injects credentials; auto_error=False keeps it None on missing/bad scheme.
    if credentials is None or not credentials.scheme.lower().startswith("bearer"):
        raise HTTPException(status_code=401, detail="missing bearer token")
    return credentials.credentials


async def require_user(token: str) -> int:
    async with httpx.AsyncClient(timeout=5) as client:
        resp = await client.post(
            f"{AUTH_URL}/api/v1/auth/validate",
            json={"token": token},
        )
    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail="invalid token")
    return int(resp.json()["user_id"])
