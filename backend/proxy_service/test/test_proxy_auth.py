from fastapi import HTTPException
from fastapi.testclient import TestClient
from pathlib import Path
from unittest.mock import AsyncMock, patch
import importlib
import importlib.util
import sys

_service_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_service_dir))
_main_path = _service_dir / "main.py"
_spec = importlib.util.spec_from_file_location(f"{_service_dir.name}_main", _main_path)
assert _spec and _spec.loader
_module = importlib.util.module_from_spec(_spec)
for k in list(sys.modules.keys()):
    if (
        k in {"api", "schema", "use_case", "util", "model", "interface", "implementation"}
        or any(k.startswith(p + ".") for p in ["api", "schema", "use_case", "util", "model", "interface", "implementation"])
    ):
        del sys.modules[k]
_spec.loader.exec_module(_module)
app = _module.app

client = TestClient(app)

auth_api = importlib.import_module("api.v1.auth")
users_api = importlib.import_module("api.v1.users")
goals_api = importlib.import_module("api.v1.goals")
tasks_api = importlib.import_module("api.v1.tasks")
notification_api = importlib.import_module("api.v1.notification")
calendar_api = importlib.import_module("api.v1.calendar")

ProxyGatewayUseCase = importlib.import_module("use_case.proxy_client").ProxyGatewayUseCase


def forward_side_effect(method: str, url: str, token=None, payload=None, x_user_id=None):  # noqa: ANN001
    if "auth/register" in url and method == "POST":
        assert payload is not None
        return {
            "user_id": 1,
            "login": payload["login"],
            "first_name": payload["first_name"],
            "last_name": payload["last_name"],
        }

    if "auth/login" in url and method == "POST":
        assert payload is not None
        if payload["password"] == "wrong":
            raise HTTPException(status_code=401, detail="invalid credentials")
        return {
            "access_token": "access_token_mock",
            "refresh_token": "refresh_token_mock",
            "token_type": "bearer",
        }

    if "auth/refresh" in url and method == "POST":
        assert payload is not None
        if payload["refresh_token"] == "bad":
            raise HTTPException(status_code=401, detail="invalid refresh token")
        return {"access_token": "access_token_refreshed_mock", "token_type": "bearer"}

    if "users/by-login" in url and method == "GET":
        login = url.split("/by-login/")[-1]
        return {"id": 1, "login": login, "first_name": "First", "last_name": "Last"}

    if "users/search" in url and method == "GET":
        mask = (payload or {}).get("mask")
        return [
            {
                "id": 1,
                "login": "mask_user@example.com",
                "first_name": "Alice" if mask and "alice" in mask.lower() else "Bob",
                "last_name": "Wonder",
            }
        ]

    if "api/v1/users" in url and method == "POST":
        assert payload is not None
        return {"id": 1, "login": payload["login"], "first_name": payload["first_name"], "last_name": payload["last_name"]}

    if "goals" in url and method == "POST":
        assert payload is not None
        return {"id": 1, "title": payload["title"], "owner_id": x_user_id}

    if "goals" in url and method == "GET":
        return [{"id": 1, "title": "Goal 1", "owner_id": x_user_id}]

    if "tasks" in url and method == "POST":
        assert payload is not None
        return {
            "id": 1,
            "goal_id": payload["goal_id"],
            "title": payload["title"],
            "owner_id": x_user_id,
            "status": payload.get("status", "new"),
        }

    if "tasks/by-goal" in url and method == "GET":
        goal_id = int(url.split("/by-goal/")[-1])
        return [
            {
                "id": 1,
                "goal_id": goal_id,
                "title": "Task 1",
                "owner_id": x_user_id,
                "status": "new",
            }
        ]

    if "tasks" in url and method == "PATCH":
        assert payload is not None
        task_id = int(url.split("/tasks/")[-1].split("/")[0])
        return {
            "id": task_id,
            "goal_id": 1,
            "title": "Task",
            "owner_id": x_user_id,
            "status": payload["status"],
        }

    if "notification" in url and method == "POST":
        return {"result": "mocked"}

    if "calendar/events" in url and method == "GET":
        return [{"id": 1, "title": "mock event"}]

    raise AssertionError(f"Unhandled forward call: {method} {url}")


def test_protected_endpoint_requires_token() -> None:
    response = client.get("/api/v1/goals")
    assert response.status_code == 401


def test_protected_endpoint_rejects_bad_header() -> None:
    response = client.get("/api/v1/goals", headers={"Authorization": "Basic abc"})
    assert response.status_code == 401


def test_auth_register_success_proxy_mock() -> None:
    with patch.object(ProxyGatewayUseCase, "forward", new=AsyncMock(side_effect=forward_side_effect)):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "login": "new_user@example.com",
                "password": "pass123",
                "first_name": "New",
                "last_name": "User",
            },
        )
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    assert data["login"] == "new_user@example.com"


def test_auth_register_invalid_email_422() -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "login": "not-email",
            "password": "pass123",
            "first_name": "New",
            "last_name": "User",
        },
    )
    assert response.status_code == 422


def test_auth_login_success_proxy_mock() -> None:
    with patch.object(ProxyGatewayUseCase, "forward", new=AsyncMock(side_effect=forward_side_effect)):
        response = client.post(
            "/api/v1/auth/login",
            json={"login": "user@example.com", "password": "pass123"},
        )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_auth_login_invalid_credentials_proxy_mock() -> None:
    with patch.object(ProxyGatewayUseCase, "forward", new=AsyncMock(side_effect=forward_side_effect)):
        response = client.post(
            "/api/v1/auth/login",
            json={"login": "user@example.com", "password": "wrong"},
        )
    assert response.status_code == 401


def test_auth_refresh_success_proxy_mock() -> None:
    with patch.object(ProxyGatewayUseCase, "forward", new=AsyncMock(side_effect=forward_side_effect)):
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "refresh_token_mock"},
        )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_auth_refresh_invalid_refresh_token_proxy_mock() -> None:
    with patch.object(ProxyGatewayUseCase, "forward", new=AsyncMock(side_effect=forward_side_effect)):
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "bad"},
        )
    assert response.status_code == 401


def test_users_by_login_requires_token() -> None:
    response = client.get("/api/v1/users/by-login/user@example.com")
    assert response.status_code == 401


def test_users_by_login_success_proxy_mock() -> None:
    with (
        patch.object(ProxyGatewayUseCase, "forward", new=AsyncMock(side_effect=forward_side_effect)),
        patch.object(users_api, "require_user", new=AsyncMock(return_value=1)),
    ):
        response = client.get(
            "/api/v1/users/by-login/user@example.com",
            headers={"Authorization": "Bearer token_mock"},
        )
    assert response.status_code == 200
    assert response.json()["login"] == "user@example.com"


def test_users_search_requires_token() -> None:
    response = client.get("/api/v1/users/search", params={"mask": "alice"})
    assert response.status_code == 401


def test_users_search_success_proxy_mock() -> None:
    with (
        patch.object(ProxyGatewayUseCase, "forward", new=AsyncMock(side_effect=forward_side_effect)),
        patch.object(users_api, "require_user", new=AsyncMock(return_value=1)),
    ):
        response = client.get(
            "/api/v1/users/search",
            params={"mask": "alice"},
            headers={"Authorization": "Bearer token_mock"},
        )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_goals_create_requires_token() -> None:
    response = client.post("/api/v1/goals", json={"title": "G"})
    assert response.status_code == 401


def test_goals_create_success_proxy_mock() -> None:
    with (
        patch.object(ProxyGatewayUseCase, "forward", new=AsyncMock(side_effect=forward_side_effect)),
        patch.object(goals_api, "require_user", new=AsyncMock(return_value=1)),
    ):
        response = client.post(
            "/api/v1/goals",
            json={"title": "G"},
            headers={"Authorization": "Bearer token_mock"},
        )
    assert response.status_code == 200
    assert response.json()["owner_id"] == 1


def test_tasks_create_requires_token() -> None:
    response = client.post("/api/v1/tasks", json={"goal_id": 1, "title": "T"})
    assert response.status_code == 401


def test_tasks_create_success_proxy_mock() -> None:
    with (
        patch.object(ProxyGatewayUseCase, "forward", new=AsyncMock(side_effect=forward_side_effect)),
        patch.object(tasks_api, "require_user", new=AsyncMock(return_value=1)),
    ):
        response = client.post(
            "/api/v1/tasks",
            json={"goal_id": 1, "title": "T"},
            headers={"Authorization": "Bearer token_mock"},
        )
    assert response.status_code == 200
    assert response.json()["owner_id"] == 1


def test_tasks_create_goal_missing_proxy_mock() -> None:
    with (
        patch.object(ProxyGatewayUseCase, "forward", new=AsyncMock(side_effect=forward_side_effect)),
        patch.object(tasks_api, "require_user", new=AsyncMock(return_value=1)),
    ):
        response = client.post(
            "/api/v1/tasks",
            json={"goal_id": 999, "title": "T"},
            headers={"Authorization": "Bearer token_mock"},
        )
    assert response.status_code == 400
    assert response.json()["detail"] == "goal not found"


def test_tasks_by_goal_requires_token() -> None:
    response = client.get("/api/v1/tasks/by-goal/1")
    assert response.status_code == 401


def test_tasks_by_goal_success_proxy_mock() -> None:
    with (
        patch.object(ProxyGatewayUseCase, "forward", new=AsyncMock(side_effect=forward_side_effect)),
        patch.object(tasks_api, "require_user", new=AsyncMock(return_value=1)),
    ):
        response = client.get(
            "/api/v1/tasks/by-goal/1",
            headers={"Authorization": "Bearer token_mock"},
        )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["goal_id"] == 1


def test_tasks_patch_requires_token() -> None:
    response = client.patch("/api/v1/tasks/1/status", json={"status": "done"})
    assert response.status_code == 401


def test_tasks_patch_success_proxy_mock() -> None:
    with (
        patch.object(ProxyGatewayUseCase, "forward", new=AsyncMock(side_effect=forward_side_effect)),
        patch.object(tasks_api, "require_user", new=AsyncMock(return_value=1)),
    ):
        response = client.patch(
            "/api/v1/tasks/1/status",
            json={"status": "done"},
            headers={"Authorization": "Bearer token_mock"},
        )
    assert response.status_code == 200
    assert response.json()["status"] == "done"


def test_notification_send_requires_token() -> None:
    response = client.post("/api/v1/notification", json={"message": "test"})
    assert response.status_code == 401


def test_notification_send_success_proxy_mock() -> None:
    with (
        patch.object(ProxyGatewayUseCase, "forward", new=AsyncMock(side_effect=forward_side_effect)),
        patch.object(notification_api, "require_user", new=AsyncMock(return_value=1)),
    ):
        response = client.post(
            "/api/v1/notification",
            json={"message": "test"},
            headers={"Authorization": "Bearer token_mock"},
        )
    assert response.status_code == 200
    assert response.json()["result"] == "mocked"


def test_calendar_events_requires_token() -> None:
    response = client.get("/api/v1/calendar/events")
    assert response.status_code == 401


def test_calendar_events_success_proxy_mock() -> None:
    with (
        patch.object(ProxyGatewayUseCase, "forward", new=AsyncMock(side_effect=forward_side_effect)),
        patch.object(calendar_api, "require_user", new=AsyncMock(return_value=1)),
    ):
        response = client.get(
            "/api/v1/calendar/events",
            headers={"Authorization": "Bearer token_mock"},
        )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["title"] == "mock event"
