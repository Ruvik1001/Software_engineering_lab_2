from pydantic import BaseModel, Field


class NotificationSendRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2048)


class NotificationSendResponse(BaseModel):
    result: str
