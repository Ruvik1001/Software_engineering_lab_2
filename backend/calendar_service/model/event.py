"""Calendar service domain models."""

from pydantic import BaseModel


class CalendarEvent(BaseModel):
    """Calendar event model."""

    id: int
    title: str
