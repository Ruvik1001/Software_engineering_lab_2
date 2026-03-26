"""Auth service application entrypoint."""

from fastapi import FastAPI
from api.v1.router import auth_router as auth_api_router

app = FastAPI(title="auth_service")
app.include_router(auth_api_router, prefix="/api/v1")

@app.get("/health")
def health() -> dict[str, str]:
    """Return service health status."""
    return {"status": "ok"}
