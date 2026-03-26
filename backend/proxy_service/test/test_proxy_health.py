from fastapi.testclient import TestClient
from pathlib import Path
import importlib
import importlib.util
import sys
from unittest.mock import patch


_service_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_service_dir))
_main_path = _service_dir / "main.py"
_spec = importlib.util.spec_from_file_location(f"{_service_dir.name}_main_health", _main_path)
assert _spec and _spec.loader
_module = importlib.util.module_from_spec(_spec)

# Ensure we execute this service's own modules (avoid cross-service import caching).
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


class _DummyResponse:
    def __init__(self, status_code: int):
        self.status_code = status_code


def _make_client(raise_on: str | None = None):
    class _DummyAsyncClient:
        def __init__(self, timeout: float = 2):  # noqa: ARG002
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001,ARG002,ARG003
            return False

        async def get(self, url: str):
            if raise_on and raise_on in url:
                raise RuntimeError("boom")
            return _DummyResponse(200)

    return _DummyAsyncClient


def test_health_json_ui_mode_0_all_ok() -> None:
    with patch.object(_module.httpx, "AsyncClient", _make_client()):
        response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["ui_mode"] == 0
    assert len(data["services"]) == 6
    assert all(item["status"] == "ok" for item in data["services"])
    assert all(isinstance(item["duration_ms"], int) for item in data["services"])


def test_health_ui_mode_1_returns_html() -> None:
    with patch.object(_module.httpx, "AsyncClient", _make_client()):
        response = client.get("/health?ui_mode=1")

    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "Lab2 microservices health" in response.text
    assert "auth_service" in response.text


def test_health_handles_service_error() -> None:
    with patch.object(_module.httpx, "AsyncClient", _make_client(raise_on="goal_service")):
        response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    goal = next(s for s in data["services"] if s["name"] == "goal_service")
    assert goal["status"] == "error"
    assert "error" in goal

