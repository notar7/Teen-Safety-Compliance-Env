from fastapi.testclient import TestClient

from server.app import app


client = TestClient(app)


def test_root_and_health():
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "running"

    h = client.get("/health")
    assert h.status_code == 200
    assert h.json()["status"] == "healthy"


def test_tasks_endpoint():
    r = client.get("/tasks")
    assert r.status_code == 200
    tasks = r.json()["tasks"]
    assert len(tasks) == 3


def test_reset_invalid_task():
    r = client.post("/reset", params={"task_id": "invalid"})
    assert r.status_code == 400


def test_reset_step_state_flow():
    r = client.post("/reset", params={"task_id": "task1_easy"})
    assert r.status_code == 200
    obs = r.json()
    assert obs["task_id"] == "task1_easy"

    action = {
        "decision": "restrict",
        "confidence": 0.8,
        "reason": "Potentially unsafe for minors.",
        "additional_action": "add_warning_label",
    }
    s = client.post("/step", json=action)
    assert s.status_code == 200
    payload = s.json()
    assert "observation" in payload and "reward" in payload
    assert isinstance(payload["done"], bool)

    state = client.get("/state")
    assert state.status_code == 200
    st = state.json()
    assert "step_number" in st
