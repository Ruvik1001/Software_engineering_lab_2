from use_case.proxy_client import ProxyGatewayUseCase
from util.config import NOTIFICATION_URL


class NotificationProxyUseCase:
    def __init__(self, gateway: ProxyGatewayUseCase) -> None:
        self._gateway = gateway

    async def send(self, token: str, payload: dict) -> dict | list:
        return await self._gateway.forward("POST", f"{NOTIFICATION_URL}/api/v1/notification", token=token, payload=payload)
