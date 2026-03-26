from fastapi import FastAPI
from api.v1.router import task_router as task_api_router

app = FastAPI(title="task_service")
app.include_router(task_api_router, prefix="/api/v1")

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
