"""Proxy service task DTOs."""

from typing import Literal

from pydantic import BaseModel, Field

TaskStatus = Literal["new", "in_progress", "done"]


class TaskCreateRequest(BaseModel):
    """Task creation request forwarded to task service."""

    goal_id: int
    title: str = Field(min_length=1, max_length=256)
    status: TaskStatus = "new"


class TaskUpdateStatusRequest(BaseModel):
    """Task status update request forwarded to task service."""

    status: TaskStatus


class TaskResponse(BaseModel):
    """Task response returned from task service."""

    id: int
    goal_id: int
    title: str
    owner_id: int
    status: TaskStatus
