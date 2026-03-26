from fastapi import FastAPI
from api.v1.router import goal_router as goal_api_router

app = FastAPI(title="goal_service")
app.include_router(goal_api_router, prefix="/api/v1")

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
