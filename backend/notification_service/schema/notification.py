from pydantic import BaseModel


class SendNotificationRequest(BaseModel):
    message: str


class SendNotificationResponse(BaseModel):
    result: str
