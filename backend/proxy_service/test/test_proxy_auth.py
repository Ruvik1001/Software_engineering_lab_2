"""Integration tests for proxy service auth and protected routes."""

from pathlib import Path
import importlib
import importlib.util
import sys
from unittest.mock import AsyncMock, patch

from fastapi import HTTPException
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

auth_api = importlib.import_module("api.v1.auth")
users_api = importlib.import_module("api.v1.users")
goals_api = importlib.import_module("api.v1.goals")
tasks_api = importlib.import_module("api.v1.tasks")
notification_api = importlib.import_module("api.v1.notification")
calendar_api = importlib.import_module("api.v1.calendar")

ProxyGatewayUseCase = importlib.import_module("use_case.proxy_client").ProxyGatewayUseCase


def _require_payload(payload: dict | None) -> dict:
    """Assert payload exists and return it."""
    assert payload is not None
    return payload


def forward_side_effect(method: str, url: str, _token=None, payload=None, x_user_id=None):  # noqa: ANN001
    """Return mocked downstream responses based on requested URL/method."""
    rules: list[tuple[str, str, callable]] = [
        (
            "POST",
            "auth/register",
            lambda: {
                "user_id": 1,
                "login": _require_payload(payload)["login"],
                "first_name": _require_payload(payload)["first_name"],
                "last_name": _require_payload(payload)["last_name"],
            },
        ),
        (
            "POST",
            "auth/login",
            lambda: (
                (_require_payload(payload)["password"] != "wrong")
                and {
                    "access_token": "access_token_mock",
                    "refresh_token": "refresh_token_mock",
                    "token_type": "bearer",
                }
                or (_raise_http(401, "invalid credentials"))
            ),
        ),
        (
            "POST",
            "auth/refresh",
            lambda: (
                (_require_payload(payload)["refresh_token"] != "bad")
                and {"access_token": "access_token_refreshed_mock", "token_type": "bearer"}
                or (_raise_http(401, "invalid refresh token"))
            ),
        ),
        (
            "GET",
            "users/by-login",
            lambda: {
                "id": 1,
                "login": url.split("/by-login/")[-1],
                "first_name": "First",
                "last_name": "Last",
            },
        ),
        (
            "GET",
            "users/search",
            lambda: [
                {
                    "id": 1,
                    "login": "mask_user@example.com",
                    "first_name": (
                        "Alice"
                        if ((payload or {}).get("mask") and "alice" in str((payload or {}).get("mask")).lower())
                        else "Bob"
                    ),
                    "last_name": "Wonder",
                }
            ],
        ),
        (
            "POST",
            "api/v1/users",
            lambda: {
                "id": 1,
                "login": _require_payload(payload)["login"],
                "first_name": _require_payload(payload)["first_name"],
                "last_name": _require_payload(payload)["last_name"],
            },
        ),
        (
            "POST",
            "goals",
            lambda: {"id": 1, "title": _require_payload(payload)["title"], "owner_id": x_user_id},
        ),
        ("GET", "goals", lambda: [{"id": 1, "title": "Goal 1", "owner_id": x_user_id}]),
        (
            "POST",
            "tasks",
            lambda: {
                "id": 1,
                "goal_id": _require_payload(payload)["goal_id"],
                "title": _require_payload(payload)["title"],
                "owner_id": x_user_id,
                "status": (_require_payload(payload).get("status", "new")),
            },
        ),
        (
            "GET",
            "tasks/by-goal",
            lambda: [
                {
                    "id": 1,
                    "goal_id": int(url.split("/by-goal/")[-1]),
                    "title": "Task 1",
                    "owner_id": x_user_id,
                    "status": "new",
                }
            ],
        ),
        (
            "PATCH",
            "tasks",
            lambda: {
                "id": int(url.split("/tasks/")[-1].split("/")[0]),
                "goal_id": 1,
                "title": "Task",
                "owner_id": x_user_id,
                "status": _require_payload(payload)["status"],
            },
        ),
        ("POST", "notification", lambda: {"result": "mocked"}),
        ("GET", "calendar/events", lambda: [{"id": 1, "title": "mock event"}]),
    ]

    for rule_method, rule_contains, factory in rules:
        if method == rule_method and rule_contains in url:
            return factory()

    raise AssertionError(f"Unhandled forward call: {method} {url}")


def _raise_http(status: int, detail: str):
    """Raise FastAPI HTTPException with given status and detail."""
    raise HTTPException(status_code=status, detail=detail)


def test_protected_endpoint_requires_token() -> None:
    """Protected endpoint requires bearer token."""
    response = client.get("/api/v1/goals")
    assert response.status_code == 401


def test_protected_endpoint_rejects_bad_header() -> None:
    """Protected endpoint rejects non-bearer Authorization."""
    response = client.get("/api/v1/goals", headers={"Authorization": "Basic abc"})
    assert response.status_code == 401


def test_auth_register_success_proxy_mock() -> None:
    """Proxy registration forwards request and returns 200."""
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
    """Proxy registration validates email and returns 422 for bad input."""
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
    """Proxy login forwards request and returns token payload."""
    with patch.object(ProxyGatewayUseCase, "forward", new=AsyncMock(side_effect=forward_side_effect)):
        response = client.post(
            "/api/v1/auth/login",
            json={"login": "user@example.com", "password": "pass123"},
        )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_auth_login_invalid_credentials_proxy_mock() -> None:
    """Proxy login propagates invalid credentials as 401."""
    with patch.object(ProxyGatewayUseCase, "forward", new=AsyncMock(side_effect=forward_side_effect)):
        response = client.post(
            "/api/v1/auth/login",
            json={"login": "user@example.com", "password": "wrong"},
        )
    assert response.status_code == 401


def test_auth_refresh_success_proxy_mock() -> None:
    """Proxy refresh forwards request and returns new access token."""
    with patch.object(ProxyGatewayUseCase, "forward", new=AsyncMock(side_effect=forward_side_effect)):
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "refresh_token_mock"},
        )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_auth_refresh_invalid_refresh_token_proxy_mock() -> None:
    """Proxy refresh propagates invalid refresh token as 401."""
    with patch.object(ProxyGatewayUseCase, "forward", new=AsyncMock(side_effect=forward_side_effect)):
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "bad"},
        )
    assert response.status_code == 401


def test_users_by_login_requires_token() -> None:
    """Users by-login endpoint requires bearer token."""
    response = client.get("/api/v1/users/by-login/user@example.com")
    assert response.status_code == 401


def test_users_by_login_success_proxy_mock() -> None:
    """Users by-login returns expected payload when authorized."""
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
    """Users search endpoint requires bearer token."""
    response = client.get("/api/v1/users/search", params={"mask": "alice"})
    assert response.status_code == 401


def test_users_search_success_proxy_mock() -> None:
    """Users search returns list payload when authorized."""
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
    """Goals create endpoint requires bearer token."""
    response = client.post("/api/v1/goals", json={"title": "G"})
    assert response.status_code == 401


def test_goals_create_success_proxy_mock() -> None:
    """Goals create returns owner_id when authorized."""
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
    """Tasks create endpoint requires bearer token."""
    response = client.post("/api/v1/tasks", json={"goal_id": 1, "title": "T"})
    assert response.status_code == 401


def test_tasks_create_success_proxy_mock() -> None:
    """Tasks create returns owner_id when authorized."""
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
    """Tasks create returns 400 if goal does not exist."""
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
    """Tasks by-goal endpoint requires bearer token."""
    response = client.get("/api/v1/tasks/by-goal/1")
    assert response.status_code == 401


def test_tasks_by_goal_success_proxy_mock() -> None:
    """Tasks by-goal returns list when authorized."""
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
    """Task status update endpoint requires bearer token."""
    response = client.patch("/api/v1/tasks/1/status", json={"status": "done"})
    assert response.status_code == 401


def test_tasks_patch_success_proxy_mock() -> None:
    """Task status update returns updated status when authorized."""
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
    """Notification endpoint requires bearer token."""
    response = client.post("/api/v1/notification", json={"message": "test"})
    assert response.status_code == 401


def test_notification_send_success_proxy_mock() -> None:
    """Notification endpoint returns mocked result when authorized."""
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
    """Calendar events endpoint requires bearer token."""
    response = client.get("/api/v1/calendar/events")
    assert response.status_code == 401


def test_calendar_events_success_proxy_mock() -> None:
    """Calendar events endpoint returns list when authorized."""
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
