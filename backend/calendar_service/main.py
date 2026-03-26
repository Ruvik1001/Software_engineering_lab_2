"""Calendar service application entrypoint (mock)."""

from fastapi import FastAPI
from api.v1.router import calendar_router as calendar_api_router

app = FastAPI(title="calendar_service")
app.include_router(calendar_api_router, prefix="/api/v1")


@app.get("/health", summary="Healthcheck", description="Calendar service health endpoint.")
def health() -> dict[str, str]:
    """Return service health status."""
    return {"status": "ok"}
