from pydantic import BaseModel


class CalendarEvent(BaseModel):
    id: int
    title: str
