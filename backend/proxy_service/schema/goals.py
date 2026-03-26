"""Proxy service goal DTOs."""

from pydantic import BaseModel, Field


class GoalCreateRequest(BaseModel):
    """Goal creation request forwarded to goal service."""

    title: str = Field(min_length=1, max_length=256)


class GoalResponse(BaseModel):
    """Goal response returned from goal service."""

    id: int
    title: str
    owner_id: int
