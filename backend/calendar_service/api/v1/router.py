"""Calendar service HTTP API routes (mock)."""

from fastapi import APIRouter

calendar_router = APIRouter(tags=["calendar"])


@calendar_router.get(
    "/calendar/events",
    summary="Mock list events",
    description="Mock endpoint for lab 2. Persistent calendar is TODO.",
)
def list_events_mock() -> list[dict]:
    """Return a mock list of calendar events."""
    return [{"id": 1, "title": "mock event"}]
