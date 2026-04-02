import re

import pytest
from fastapi.testclient import TestClient

from server.app import app


client = TestClient(app)


def test_root_contract_fields():
    r = client.get("/")
    assert r.status_code == 200
    body = r.json()

    required = {"name", "status", "version", "team", "hackathon", "docs"}
    assert required.issubset(body.keys())
    assert body["docs"] == "/docs"


def test_health_contract_fields():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert set(body.keys()) == {"status"}


def test_tasks_contract_shape_and_values():
    r = client.get("/tasks")
    assert r.status_code == 200
    tasks = r.json()["tasks"]
    assert len(tasks) == 3

    for t in tasks:
        required = {"id", "name", "difficulty", "description", "expected_score_range", "num_scenarios"}
        assert required.issubset(t.keys())
        assert t["difficulty"] in {"easy", "medium", "hard"}
        assert re.match(r"^\d\.\d{2}\s-\s\d\.\d{2}$", t["expected_score_range"]) is not None


def test_reset_default_task_is_task1_easy():
    r = client.post("/reset")
    assert r.status_code == 200
    obs = r.json()
    assert obs["task_id"] == "task1_easy"


@pytest.mark.parametrize("bad_task", ["bad", "task4", ""]) 
def test_reset_invalid_task_ids_return_400(bad_task):
    r = client.post("/reset", params={"task_id": bad_task})
    assert r.status_code == 400


@pytest.mark.parametrize("task_id", ["task1_easy", "task2_medium", "task3_hard"])
def test_step_response_contract_for_each_task(task_id):
    r = client.post("/reset", params={"task_id": task_id})
    assert r.status_code == 200

    action = {
        "decision": "restrict",
        "confidence": 0.75,
        "reason": "Potential safety risk for minors.",
        "additional_action": "add_warning_label",
    }
    s = client.post("/step", json=action)
    assert s.status_code == 200
    body = s.json()

    assert set(body.keys()) == {"observation", "reward", "done", "info"}
    assert isinstance(body["done"], bool)
    assert "score" in body["reward"]
    assert 0.0 <= body["reward"]["score"] <= 1.0


def test_state_contract_after_reset():
    r = client.post("/reset", params={"task_id": "task3_hard"})
    assert r.status_code == 200

    st = client.get("/state")
    assert st.status_code == 200
    body = st.json()

    required = {
        "task_id",
        "case_id",
        "case_type",
        "platform_context",
        "user_profile",
        "step_number",
        "previous_actions",
        "episode_scores",
        "episode_done",
    }
    assert required.issubset(body.keys())
    assert body["task_id"] == "task3_hard"
