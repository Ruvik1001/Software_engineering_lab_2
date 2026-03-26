from use_case.proxy_client import ProxyGatewayUseCase
from util.config import CALENDAR_URL


class CalendarProxyUseCase:
    def __init__(self, gateway: ProxyGatewayUseCase) -> None:
        self._gateway = gateway

    async def list_events(self, token: str) -> dict | list:
        return await self._gateway.forward("GET", f"{CALENDAR_URL}/api/v1/calendar/events", token=token)
