"""Proxy use-case for user-related operations."""

from use_case.proxy_client import ProxyGatewayUseCase
from util.config import USER_URL


class UserProxyUseCase:
    """Forwards user requests to user_service."""

    def __init__(self, gateway: ProxyGatewayUseCase) -> None:
        """Create use-case with provided gateway."""
        self._gateway = gateway

    async def create_user(self, token: str, payload: dict) -> dict | list:
        """Forward user creation."""
        return await self._gateway.forward("POST", f"{USER_URL}/api/v1/users", token=token, payload=payload)

    async def by_login(self, token: str, login: str) -> dict | list:
        """Forward get user by login."""
        return await self._gateway.forward("GET", f"{USER_URL}/api/v1/users/by-login/{login}", token=token)

    async def search(self, token: str, mask: str) -> dict | list:
        """Forward user search by name mask."""
        return await self._gateway.forward(
            "GET",
            f"{USER_URL}/api/v1/users/search",
            token=token,
            payload={"mask": mask},
        )
