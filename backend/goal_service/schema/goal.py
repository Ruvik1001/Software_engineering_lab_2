"""Goal service request/response DTOs."""

from pydantic import BaseModel, Field


class CreateGoalRequest(BaseModel):
    """Goal creation request payload."""

    title: str = Field(min_length=1, max_length=256)


class GoalResponse(BaseModel):
    """Goal response payload."""

    id: int
    title: str
    owner_id: int
