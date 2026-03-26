"""Proxy goal routes."""

from fastapi import APIRouter, Depends

from use_case.goal_proxy import GoalProxyUseCase
from util.auth import get_token_value, require_user
from util.dependencies import get_goal_proxy_use_case
from schema.goals import GoalCreateRequest, GoalResponse

goal_proxy_router = APIRouter(prefix="/goals", tags=["proxy-goals"])


@goal_proxy_router.post(
    "",
    summary="Proxy: create goal",
    description="Authorized route. Creates goal in goal service.",
    response_model=GoalResponse,
)
async def create_goal(
    body: GoalCreateRequest,
    token: str = Depends(get_token_value),
    use_case: GoalProxyUseCase = Depends(get_goal_proxy_use_case),
) -> GoalResponse:
    """Authorize and create goal via goal service."""
    user_id = await require_user(token)
    return await use_case.create_goal(token=token, user_id=user_id, payload=body.model_dump())


@goal_proxy_router.get(
    "",
    summary="Proxy: list goals",
    description="Authorized route. Returns goals from goal service.",
    response_model=list[GoalResponse],
)
async def list_goals(
    token: str = Depends(get_token_value),
    use_case: GoalProxyUseCase = Depends(get_goal_proxy_use_case),
) -> list[GoalResponse]:
    """Authorize and list goals via goal service."""
    user_id = await require_user(token)
    return await use_case.list_goals(token=token, user_id=user_id)
