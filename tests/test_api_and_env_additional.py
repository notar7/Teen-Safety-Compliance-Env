import pytest
from fastapi.testclient import TestClient

from env.environment import TeenSafetyEnvironment
from env.models import TeenSafetyAction
from server.app import app


client = TestClient(app)


@pytest.mark.parametrize("task_id", ["task1_easy", "task2_medium", "task3_hard"])
def test_reset_works_for_each_task(task_id):
    r = client.post("/reset", params={"task_id": task_id})
    assert r.status_code == 200
    body = r.json()
    assert body["task_id"] == task_id
    assert "case_id" in body


def test_step_invalid_payload_returns_422():
    r = client.post("/step", json={"decision": "allow"})
    assert r.status_code == 422


def test_state_updates_after_step():
    r = client.post("/reset", params={"task_id": "task2_medium"})
    assert r.status_code == 200

    action = {
        "decision": "restrict",
        "confidence": 0.7,
        "reason": "Potential teen harm risk in this content.",
        "additional_action": "add_warning_label",
    }
    s = client.post("/step", json=action)
    assert s.status_code == 200

    st = client.get("/state")
    assert st.status_code == 200
    state = st.json()
    assert state["step_number"] >= 1
    assert len(state["previous_actions"]) >= 1


@pytest.mark.parametrize("task_id", ["task1_easy", "task2_medium", "task3_hard"])
def test_environment_reset_state_contains_expected_fields(task_id):
    env = TeenSafetyEnvironment(rng_seed=123)
    obs = env.reset(task_id)
    state = env.state()

    assert obs.task_id == task_id
    assert state["task_id"] == task_id
    assert "case_id" in state
    assert "episode_scores" in state


def test_environment_done_within_max_steps():
    env = TeenSafetyEnvironment(rng_seed=7)
    env.reset("task1_easy")

    action = TeenSafetyAction(
        decision="restrict",
        confidence=0.7,
        reason="Potentially unsafe for minors.",
        additional_action="add_warning_label",
    )

    done = False
    steps = 0
    while not done and steps <= env.MAX_STEPS:
        _, _, done, _ = env.step(action)
        steps += 1

    assert done is True
    assert steps <= env.MAX_STEPS
