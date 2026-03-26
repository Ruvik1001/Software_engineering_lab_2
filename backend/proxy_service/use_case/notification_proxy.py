"""Proxy use-case for notification-related operations."""

from use_case.proxy_client import ProxyGatewayUseCase
from util.config import NOTIFICATION_URL


class NotificationProxyUseCase:
    """Forwards notification requests to notification_service."""

    def __init__(self, gateway: ProxyGatewayUseCase) -> None:
        """Create use-case with provided gateway."""
        self._gateway = gateway

    async def send(self, token: str, payload: dict) -> dict | list:
        """Forward send notification request."""
        return await self._gateway.forward(
            "POST",
            f"{NOTIFICATION_URL}/api/v1/notification",
            token=token,
            payload=payload,
        )
