"""Proxy use-case for auth-related operations."""

from use_case.proxy_client import ProxyGatewayUseCase
from util.config import AUTH_URL, USER_URL


class AuthProxyUseCase:
    """Forwards auth requests to auth_service and syncs user_service."""

    def __init__(self, gateway: ProxyGatewayUseCase) -> None:
        """Create use-case with provided gateway."""
        self._gateway = gateway

    async def register(self, payload: dict) -> dict | list:
        """Register in auth service and create profile in user service."""
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
        """Forward login request to auth service."""
        return await self._gateway.forward("POST", f"{AUTH_URL}/api/v1/auth/login", payload=payload)

    async def refresh(self, payload: dict) -> dict | list:
        """Forward refresh request to auth service."""
        return await self._gateway.forward("POST", f"{AUTH_URL}/api/v1/auth/refresh", payload=payload)
