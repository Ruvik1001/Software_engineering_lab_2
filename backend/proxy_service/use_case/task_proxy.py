from fastapi import HTTPException

from use_case.proxy_client import ProxyGatewayUseCase
from util.config import GOAL_URL, TASK_URL


class TaskProxyUseCase:
    def __init__(self, gateway: ProxyGatewayUseCase) -> None:
        self._gateway = gateway

    async def create_task(self, token: str, user_id: int, payload: dict) -> dict | list:
        goal_id = payload.get("goal_id")
        # Validate goal existence/ownership to prevent "orphan" tasks.
        goals = await self._gateway.forward("GET", f"{GOAL_URL}/api/v1/goals", x_user_id=user_id)
        goal_ids = {g.get("id") for g in goals if isinstance(g, dict)}
        if goal_id not in goal_ids:
            raise HTTPException(status_code=400, detail="goal not found")

        return await self._gateway.forward(
            "POST",
            f"{TASK_URL}/api/v1/tasks",
            token=token,
            x_user_id=user_id,
            payload=payload,
        )

    async def by_goal(self, token: str, user_id: int, goal_id: int) -> dict | list:
        return await self._gateway.forward(
            "GET",
            f"{TASK_URL}/api/v1/tasks/by-goal/{goal_id}",
            token=token,
            x_user_id=user_id,
        )

    async def update_status(
        self,
        token: str,
        user_id: int,
        task_id: int,
        payload: dict,
    ) -> dict | list:
        return await self._gateway.forward(
            "PATCH",
            f"{TASK_URL}/api/v1/tasks/{task_id}/status",
            token=token,
            x_user_id=user_id,
            payload=payload,
        )
