from fastapi import APIRouter, Depends

from schema.goal import CreateGoalRequest, GoalResponse
from use_case.service import GoalService
from util.dependencies import get_goal_service, get_owner_id

goal_router = APIRouter(tags=["goals"])


@goal_router.post(
    "/goals",
    response_model=GoalResponse,
    summary="Create goal",
    description="Creates a planning goal for an executor.",
)
def create(
    req: CreateGoalRequest,
    owner_id: int = Depends(get_owner_id),
    service: GoalService = Depends(get_goal_service),
) -> GoalResponse:
    return GoalResponse.model_validate(service.create_goal(title=req.title, owner_id=owner_id))


@goal_router.get(
    "/goals",
    response_model=list[GoalResponse],
    summary="List goals",
    description="Returns all goals currently stored in memory.",
)
def list_all(
    owner_id: int = Depends(get_owner_id),
    service: GoalService = Depends(get_goal_service),
) -> list[GoalResponse]:
    return [GoalResponse.model_validate(item) for item in service.list_goals(owner_id)]
