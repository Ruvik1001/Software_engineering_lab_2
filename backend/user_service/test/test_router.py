"""Integration tests for user service HTTP API."""

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


def test_create_and_get_user() -> None:
    """Create user and fetch by login."""
    created = client.post(
        "/api/v1/users",
        json={"login": "john@example.com", "first_name": "John", "last_name": "Doe"},
    )
    assert created.status_code == 200

    fetched = client.get("/api/v1/users/by-login/john@example.com")
    assert fetched.status_code == 200
    assert fetched.json()["first_name"] == "John"


def test_user_not_found() -> None:
    """Fetching unknown user returns 404."""
    response = client.get("/api/v1/users/by-login/unknown@example.com")
    assert response.status_code == 404


def test_create_duplicate_user() -> None:
    """Creating duplicate login returns 400."""
    client.post(
        "/api/v1/users",
        json={"login": "dup_user@example.com", "first_name": "A", "last_name": "B"},
    )
    duplicate = client.post(
        "/api/v1/users",
        json={"login": "dup_user@example.com", "first_name": "A", "last_name": "B"},
    )
    assert duplicate.status_code == 400


def test_create_user_invalid_email() -> None:
    """Invalid email yields 422."""
    created = client.post(
        "/api/v1/users",
        json={"login": "not-an-email", "first_name": "A", "last_name": "B"},
    )
    assert created.status_code == 422


def test_search_users_by_mask() -> None:
    """Search by mask returns created user."""
    login = "mask_user@example.com"
    client.post("/api/v1/users", json={"login": login, "first_name": "Alice", "last_name": "Wonder"})
    response = client.get("/api/v1/users/search", params={"mask": "alice"})
    assert response.status_code == 200
    payload = response.json()
    assert any(u["login"] == login for u in payload)


def test_search_users_by_mask_validation_error() -> None:
    """Empty mask yields 422."""
    response = client.get("/api/v1/users/search", params={"mask": ""})
    assert response.status_code == 422
