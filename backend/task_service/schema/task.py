from pydantic import BaseModel, Field


class CreateTaskRequest(BaseModel):
    goal_id: int
    title: str = Field(min_length=1, max_length=256)
    status: str = "new"


class UpdateStatusRequest(BaseModel):
    status: str


class TaskResponse(BaseModel):
    id: int
    goal_id: int
    title: str
    owner_id: int
    status: str
