from fastapi.testclient import TestClient
from pathlib import Path
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

def test_mock_notification_endpoint():
    response = client.post("/api/v1/notification", json={"message": "test"})
    assert response.status_code == 200


def test_mock_notification_endpoint_second_message():
    response = client.post("/api/v1/notification", json={"message": "hello"})
    assert response.status_code == 200
    assert response.json()["result"] == "mocked"
