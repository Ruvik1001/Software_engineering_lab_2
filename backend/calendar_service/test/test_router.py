"""Integration tests for calendar service mock API."""

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

def test_mock_calendar_events():
    """GET /calendar/events returns 200."""
    response = client.get("/api/v1/calendar/events")
    assert response.status_code == 200


def test_mock_calendar_events_response_shape():
    """GET /calendar/events returns a list of objects with id/title."""
    response = client.get("/api/v1/calendar/events")
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload
    assert "id" in payload[0]
    assert "title" in payload[0]
