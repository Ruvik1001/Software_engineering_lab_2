"""Proxy use-case for calendar-related operations."""

from use_case.proxy_client import ProxyGatewayUseCase
from util.config import CALENDAR_URL


class CalendarProxyUseCase:
    """Forwards calendar requests to calendar_service."""

    def __init__(self, gateway: ProxyGatewayUseCase) -> None:
        """Create use-case with provided gateway."""
        self._gateway = gateway

    async def list_events(self, token: str) -> dict | list:
        """Forward list events request."""
        return await self._gateway.forward("GET", f"{CALENDAR_URL}/api/v1/calendar/events", token=token)
