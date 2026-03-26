from use_case.proxy_client import ProxyGatewayUseCase
from util.config import AUTH_URL, USER_URL


class AuthProxyUseCase:
    def __init__(self, gateway: ProxyGatewayUseCase) -> None:
        self._gateway = gateway

    async def register(self, payload: dict) -> dict | list:
        auth_resp = await self._gateway.forward("POST", f"{AUTH_URL}/api/v1/auth/register", payload=payload)
        # Keep auth credentials and user profile in sync.
        user_payload = {
            "login": payload["login"],
            "first_name": payload["first_name"],
            "last_name": payload["last_name"],
        }
        await self._gateway.forward("POST", f"{USER_URL}/api/v1/users", payload=user_payload)
        return auth_resp

    async def login(self, payload: dict) -> dict | list:
        return await self._gateway.forward("POST", f"{AUTH_URL}/api/v1/auth/login", payload=payload)

    async def refresh(self, payload: dict) -> dict | list:
        return await self._gateway.forward("POST", f"{AUTH_URL}/api/v1/auth/refresh", payload=payload)
