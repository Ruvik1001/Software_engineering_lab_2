from typing import Literal

from pydantic import BaseModel, Field

TaskStatus = Literal["new", "in_progress", "done"]


class TaskCreateRequest(BaseModel):
    goal_id: int
    title: str = Field(min_length=1, max_length=256)
    status: TaskStatus = "new"


class TaskUpdateStatusRequest(BaseModel):
    status: TaskStatus


class TaskResponse(BaseModel):
    id: int
    goal_id: int
    title: str
    owner_id: int
    status: TaskStatus
