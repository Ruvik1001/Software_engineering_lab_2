from pydantic import BaseModel, Field


class GoalCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=256)


class GoalResponse(BaseModel):
    id: int
    title: str
    owner_id: int
