"""Notification service request/response DTOs (mock)."""

from pydantic import BaseModel


class SendNotificationRequest(BaseModel):
    """Notification send request."""

    message: str


class SendNotificationResponse(BaseModel):
    """Notification send response."""

    result: str
