"""Proxy service notification DTOs."""

from pydantic import BaseModel, Field


class NotificationSendRequest(BaseModel):
    """Notification send request forwarded to notification service."""

    message: str = Field(min_length=1, max_length=2048)


class NotificationSendResponse(BaseModel):
    """Notification send response returned from notification service."""

    result: str
