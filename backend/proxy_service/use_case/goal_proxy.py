"""Proxy use-case for goal-related operations."""

from use_case.proxy_client import ProxyGatewayUseCase
from util.config import GOAL_URL


class GoalProxyUseCase:
    """Forwards goal requests to goal_service."""

    def __init__(self, gateway: ProxyGatewayUseCase) -> None:
        """Create use-case with provided gateway."""
        self._gateway = gateway

    async def create_goal(self, token: str, user_id: int, payload: dict) -> dict | list:
        """Forward goal creation to goal service."""
        return await self._gateway.forward(
            "POST",
            f"{GOAL_URL}/api/v1/goals",
            token=token,
            x_user_id=user_id,
            payload=payload,
        )

    async def list_goals(self, token: str, user_id: int) -> dict | list:
        """Forward goal list request to goal service."""
        return await self._gateway.forward(
            "GET",
            f"{GOAL_URL}/api/v1/goals",
            token=token,
            x_user_id=user_id,
        )
