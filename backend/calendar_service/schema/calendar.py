"""Calendar service request/response DTOs."""

from pydantic import BaseModel


class CalendarEventResponse(BaseModel):
    """Calendar event response DTO."""

    id: int
    title: str
