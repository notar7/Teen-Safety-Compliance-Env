import pytest

from env.environment import TeenSafetyEnvironment
from env.models import TeenSafetyAction


def _safe_action():
    return TeenSafetyAction(
        decision="restrict",
        confidence=0.7,
        reason="Potentially unsafe for teen audience based on policy.",
        additional_action="add_warning_label",
    )


def test_step_before_reset_raises():
    env = TeenSafetyEnvironment(rng_seed=42)
    with pytest.raises(RuntimeError):
        env.step(_safe_action())


def test_reset_invalid_task_raises():
    env = TeenSafetyEnvironment(rng_seed=42)
    with pytest.raises(ValueError):
        env.reset("bad_task")


def test_environment_episode_flow():
    env = TeenSafetyEnvironment(rng_seed=42)
    obs = env.reset("task1_easy")
    assert obs.task_id == "task1_easy"

    done = False
    steps = 0
    while not done and steps < env.MAX_STEPS:
        _, reward, done, info = env.step(_safe_action())
        assert 0.0 <= reward.score <= 1.0
        assert info["task_id"] == "task1_easy"
        steps += 1

    assert steps >= 1
    assert done is True or steps == env.MAX_STEPS
