"""Notification service domain models (mock)."""

from pydantic import BaseModel


class Notification(BaseModel):
    """Notification payload model."""

    message: str
