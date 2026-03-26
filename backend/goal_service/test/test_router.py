"""Integration tests for goal service HTTP API."""

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


def test_create_and_list_goals() -> None:
    """Create goal and verify it appears in owner's list."""
    created = client.post(
        "/api/v1/goals",
        json={"title": "Learn FastAPI"},
        headers={"X-User-Id": "1"},
    )
    assert created.status_code == 200

    listed = client.get("/api/v1/goals", headers={"X-User-Id": "1"})
    assert listed.status_code == 200
    assert any(goal["title"] == "Learn FastAPI" for goal in listed.json())

    other_listed = client.get("/api/v1/goals", headers={"X-User-Id": "2"})
    assert other_listed.status_code == 200
    assert not any(goal["title"] == "Learn FastAPI" for goal in other_listed.json())


def test_create_goal_validation_error() -> None:
    """Empty title triggers validation error (422)."""
    response = client.post("/api/v1/goals", json={"title": ""}, headers={"X-User-Id": "1"})
    assert response.status_code == 422


def test_missing_x_user_id() -> None:
    """Missing X-User-Id header returns 401."""
    response_post = client.post("/api/v1/goals", json={"title": "T"})
    assert response_post.status_code == 401

    response_get = client.get("/api/v1/goals")
    assert response_get.status_code == 401
