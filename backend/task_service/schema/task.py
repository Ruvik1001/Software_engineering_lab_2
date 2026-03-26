"""Task service request/response DTOs."""

from pydantic import BaseModel, Field


class CreateTaskRequest(BaseModel):
    """Task creation request payload."""

    goal_id: int
    title: str = Field(min_length=1, max_length=256)
    status: str = "new"


class UpdateStatusRequest(BaseModel):
    """Task status update request payload."""

    status: str


class TaskResponse(BaseModel):
    """Task response payload."""

    id: int
    goal_id: int
    title: str
    owner_id: int
    status: str
