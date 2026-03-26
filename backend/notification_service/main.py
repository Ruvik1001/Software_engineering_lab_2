"""Notification service application entrypoint (mock)."""

from fastapi import FastAPI
from api.v1.router import notification_router as notification_api_router

app = FastAPI(title="notification_service")
app.include_router(notification_api_router, prefix="/api/v1")


@app.get("/health", summary="Healthcheck", description="Notification service health endpoint.")
def health() -> dict[str, str]:
    """Return service health status."""
    return {"status": "ok"}
