from use_case.proxy_client import ProxyGatewayUseCase
from util.config import USER_URL


class UserProxyUseCase:
    def __init__(self, gateway: ProxyGatewayUseCase) -> None:
        self._gateway = gateway

    async def create_user(self, token: str, payload: dict) -> dict | list:
        return await self._gateway.forward("POST", f"{USER_URL}/api/v1/users", token=token, payload=payload)

    async def by_login(self, token: str, login: str) -> dict | list:
        return await self._gateway.forward("GET", f"{USER_URL}/api/v1/users/by-login/{login}", token=token)

    async def search(self, token: str, mask: str) -> dict | list:
        return await self._gateway.forward("GET", f"{USER_URL}/api/v1/users/search", token=token, payload={"mask": mask})
