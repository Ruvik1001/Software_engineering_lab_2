from pydantic import BaseModel


class CalendarEventResponse(BaseModel):
    id: int
    title: str
