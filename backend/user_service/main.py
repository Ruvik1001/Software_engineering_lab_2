"""User service application entrypoint."""

from fastapi import FastAPI
from api.v1.router import user_router as user_api_router

app = FastAPI(title="user_service")
app.include_router(user_api_router, prefix="/api/v1")

@app.get("/health")
def health() -> dict[str, str]:
    """Return service health status."""
    return {"status": "ok"}
