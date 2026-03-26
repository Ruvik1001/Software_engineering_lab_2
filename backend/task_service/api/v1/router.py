from fastapi import APIRouter, Depends, HTTPException

from schema.task import CreateTaskRequest, TaskResponse, UpdateStatusRequest
from use_case.service import TaskService
from util.dependencies import get_owner_id, get_task_service

task_router = APIRouter(tags=["tasks"])


@task_router.post(
    "/tasks",
    response_model=TaskResponse,
    summary="Create task",
    description="Creates a task that belongs to a goal.",
    responses={400: {"description": "Invalid status"}},
)
def create(
    req: CreateTaskRequest,
    owner_id: int = Depends(get_owner_id),
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    try:
        return TaskResponse.model_validate(service.create_task(req.model_dump(), owner_id))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@task_router.get(
    "/tasks/by-goal/{goal_id}",
    response_model=list[TaskResponse],
    summary="List goal tasks",
    description="Returns all tasks assigned to the goal.",
)
def by_goal(
    goal_id: int,
    owner_id: int = Depends(get_owner_id),
    service: TaskService = Depends(get_task_service),
) -> list[TaskResponse]:
    return [TaskResponse.model_validate(item) for item in service.get_tasks(goal_id, owner_id)]


@task_router.patch(
    "/tasks/{task_id}/status",
    response_model=TaskResponse,
    summary="Update task status",
    description="Changes task status to new, in_progress or done.",
    responses={400: {"description": "Invalid status"}, 404: {"description": "Task not found"}},
)
def patch_status(
    task_id: int,
    req: UpdateStatusRequest,
    owner_id: int = Depends(get_owner_id),
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    try:
        task = service.update_status(task_id, owner_id, req.status)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    return TaskResponse.model_validate(task)
