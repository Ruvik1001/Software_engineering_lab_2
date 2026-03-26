"""Notification service HTTP API routes (mock)."""

from fastapi import APIRouter

notification_router = APIRouter(tags=["notification"])


@notification_router.post(
    "/notification",
    summary="Mock send notification",
    description="Mock endpoint for lab 2. Real provider integration is TODO.",
)
def send_mock() -> dict[str, str]:
    """Return mock notification delivery result."""
    return {"result": "mocked"}
