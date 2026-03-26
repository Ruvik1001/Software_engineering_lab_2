"""Integration tests for auth service HTTP API."""

from pathlib import Path
import importlib.util
import os
import sys

from fastapi.testclient import TestClient

_service_dir = Path(__file__).resolve().parents[1]

# Tests must be deterministic and not rely on external env injection.
# We read secrets only from the service's .env_example.
_env_example_path = _service_dir / ".env_example"
if _env_example_path.exists():
    for raw_line in _env_example_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)

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


def test_register_and_login_success() -> None:
    """Register user and login returns access token."""
    register = client.post(
        "/api/v1/auth/register",
        json={
            "login": "owner@example.com",
            "password": "pass123",
            "first_name": "Own",
            "last_name": "Er",
        },
    )
    assert register.status_code == 200

    login = client.post(
        "/api/v1/auth/login",
        json={"login": "owner@example.com", "password": "pass123"},
    )
    assert login.status_code == 200
    assert "access_token" in login.json()


def test_register_duplicate_login() -> None:
    """Registering same login twice returns 400."""
    client.post(
        "/api/v1/auth/register",
        json={"login": "dup@example.com", "password": "pass", "first_name": "A", "last_name": "B"},
    )
    duplicate = client.post(
        "/api/v1/auth/register",
        json={"login": "dup@example.com", "password": "pass", "first_name": "A", "last_name": "B"},
    )
    assert duplicate.status_code == 400


def test_refresh_with_access_token_fails() -> None:
    """Refreshing with access token must fail."""
    client.post(
        "/api/v1/auth/register",
        json={"login": "r1_refresh@example.com", "password": "pass", "first_name": "A", "last_name": "B"},
    )
    login = client.post("/api/v1/auth/login", json={"login": "r1_refresh@example.com", "password": "pass"})
    assert login.status_code == 200
    bad = client.post("/api/v1/auth/refresh", json={"refresh_token": login.json()["access_token"]})
    assert bad.status_code == 401


def test_register_invalid_email() -> None:
    """Invalid email in login field yields 422."""
    response = client.post(
        "/api/v1/auth/register",
        json={"login": "not-an-email", "password": "pass123", "first_name": "A", "last_name": "B"},
    )
    assert response.status_code == 422


def test_validate_invalid_token() -> None:
    """Validating a bad token yields 401."""
    response = client.post("/api/v1/auth/validate", json={"token": "bad-token"})
    assert response.status_code == 401


def test_validate_success() -> None:
    """Valid token validates and returns integer user_id."""
    client.post(
        "/api/v1/auth/register",
        json={"login": "val_success@example.com", "password": "pass123", "first_name": "A", "last_name": "B"},
    )
    login = client.post(
        "/api/v1/auth/login",
        json={"login": "val_success@example.com", "password": "pass123"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    response = client.post("/api/v1/auth/validate", json={"token": token})
    assert response.status_code == 200
    assert isinstance(response.json()["user_id"], int)


def test_refresh_invalid_token() -> None:
    """Refreshing with invalid refresh token yields 401."""
    response = client.post("/api/v1/auth/refresh", json={"refresh_token": "bad-refresh-token"})
    assert response.status_code == 401
