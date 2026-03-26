"""Proxy service calendar DTOs."""

from pydantic import BaseModel


class CalendarEventResponse(BaseModel):
    """Calendar event response returned from calendar service."""

    id: int
    title: str
