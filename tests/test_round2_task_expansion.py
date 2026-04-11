from fastapi.testclient import TestClient

from env.environment import TeenSafetyEnvironment, get_task_ids
from env.models import TeenSafetyAction
from server.app import app


client = TestClient(app)


def test_task_catalog_expanded_to_ten_tasks():
    task_ids = get_task_ids()
    assert len(task_ids) >= 10
    assert {"task4_easy", "task7_medium", "task10_hard"}.issubset(set(task_ids))


def test_server_tasks_endpoint_includes_new_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200

    tasks = response.json()["tasks"]
    task_ids = {t["id"] for t in tasks}
    assert {"task4_easy", "task5_easy", "task6_medium", "task9_hard", "task10_hard"}.issubset(task_ids)


def test_environment_reset_supports_new_tasks():
    env = TeenSafetyEnvironment(rng_seed=99)

    for task_id in ["task4_easy", "task6_medium", "task8_medium", "task10_hard"]:
        obs = env.reset(task_id)
        assert obs.task_id == task_id


def test_step_scores_for_new_tasks_remain_in_open_interval():
    env = TeenSafetyEnvironment(rng_seed=42)
    env.reset("task9_hard")

    action = TeenSafetyAction(
        decision="restrict",
        confidence=0.66,
        reason="Mixed adversarial cues with teen-targeting context, restricting pending further review.",
        additional_action="add_warning_label",
    )

    _, reward, _, info = env.step(action)

    assert 0.0 < reward.score < 1.0
    assert 0.0 < info["episode_reward"] < 1.0
