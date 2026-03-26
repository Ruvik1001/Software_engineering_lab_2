from pydantic import BaseModel, Field


class CreateGoalRequest(BaseModel):
    title: str = Field(min_length=1, max_length=256)


class GoalResponse(BaseModel):
    id: int
    title: str
    owner_id: int
