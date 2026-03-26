"""Integration tests for task service HTTP API."""

from pathlib import Path
import importlib.util
import sys

from fastapi.testclient import TestClient

_service_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_service_dir))
_main_path = _service_dir / "main.py"
_spec = importlib.util.spec_from_file_location(f"{_service_dir.name}_main", _main_path)
assert _spec and _spec.loader
_module = importlib.util.module_from_spec(_spec)
for k in list(sys.modules.keys()):
    if (
        k in {"api", "schema", "use_case", "util", "model", "interface", "implementation"}
        or any(
            k.startswith(p + ".")
            for p in ["api", "schema", "use_case", "util", "model", "interface", "implementation"]
        )
    ):
        del sys.modules[k]
_spec.loader.exec_module(_module)
app = _module.app

client = TestClient(app)


def test_task_lifecycle() -> None:
    """Create task, list by goal, update status, and enforce ownership."""
    created = client.post(
        "/api/v1/tasks",
        json={"goal_id": 1, "title": "Task 1"},
        headers={"X-User-Id": "1"},
    )
    assert created.status_code == 200
    task_id = created.json()["id"]

    listed = client.get("/api/v1/tasks/by-goal/1", headers={"X-User-Id": "1"})
    assert listed.status_code == 200
    assert len(listed.json()) >= 1

    updated = client.patch(
        f"/api/v1/tasks/{task_id}/status",
        json={"status": "done"},
        headers={"X-User-Id": "1"},
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "done"

    other_listed = client.get("/api/v1/tasks/by-goal/1", headers={"X-User-Id": "2"})
    assert other_listed.status_code == 200
    assert len(other_listed.json()) == 0

    other_update = client.patch(
        f"/api/v1/tasks/{task_id}/status",
        json={"status": "done"},
        headers={"X-User-Id": "2"},
    )
    assert other_update.status_code == 404


def test_invalid_status_on_create() -> None:
    """Creating a task with invalid status returns 400."""
    response = client.post(
        "/api/v1/tasks",
        json={"goal_id": 1, "title": "T", "status": "bad"},
        headers={"X-User-Id": "1"},
    )
    assert response.status_code == 400


def test_update_missing_task() -> None:
    """Updating a non-existing task returns 404."""
    response = client.patch(
        "/api/v1/tasks/9999/status",
        json={"status": "done"},
        headers={"X-User-Id": "1"},
    )
    assert response.status_code == 404


def test_missing_x_user_id() -> None:
    """Missing X-User-Id header returns 401."""
    response_post = client.post("/api/v1/tasks", json={"goal_id": 1, "title": "T"})
    assert response_post.status_code == 401

    response_patch = client.patch("/api/v1/tasks/1/status", json={"status": "done"})
    assert response_patch.status_code == 401


def test_tasks_by_goal_missing_x_user_id() -> None:
    """Missing X-User-Id header returns 401 for list endpoint."""
    response = client.get("/api/v1/tasks/by-goal/1")
    assert response.status_code == 401
