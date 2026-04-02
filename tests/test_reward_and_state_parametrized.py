import pytest

from env.reward import RewardCalculator
from env.state_manager import StateManager


@pytest.mark.parametrize(
    "score, expected_fragment",
    [
        (0.95, "Excellent decision"),
        (0.75, "Good decision"),
        (0.55, "Partially correct"),
        (0.35, "Mostly incorrect"),
        (0.10, "Incorrect decision"),
    ],
)
def test_reward_feedback_tiers(score, expected_fragment):
    rc = RewardCalculator()
    reward = rc.compute(
        score=score,
        action={"decision": "restrict", "confidence": 0.7, "reason": "reason", "additional_action": None},
        ground_truth={"correct_decision": "block", "acceptable_decisions": ["restrict"], "explanation": "Policy says block this content for minors."},
        task_id="task1_easy",
    )
    assert expected_fragment in reward.feedback


@pytest.mark.parametrize(
    "agent_decision, expected_match",
    [
        ("block", "correct"),
        ("restrict", "acceptable"),
        ("allow", "wrong"),
    ],
)
def test_breakdown_decision_match(agent_decision, expected_match):
    rc = RewardCalculator()
    reward = rc.compute(
        score=0.5,
        action={"decision": agent_decision, "confidence": 0.6, "reason": "some reason", "additional_action": None},
        ground_truth={"correct_decision": "block", "acceptable_decisions": ["restrict"], "explanation": "x"},
        task_id="task1_easy",
    )
    assert reward.breakdown["decision_match"] == expected_match


def test_state_manager_copy_isolated_from_mutation():
    sm = StateManager()
    sm.set_state(
        {
            "case_id": "T1_001",
            "case_type": "content_review",
            "platform_context": "instagram",
            "user_profile": {"declared_age": 15},
        },
        "task1_easy",
    )

    state = sm.get_state()
    state["task_id"] = "tampered"
    assert sm.get_state()["task_id"] == "task1_easy"


@pytest.mark.parametrize("steps", [1, 2, 3, 4])
def test_state_manager_step_counter_and_scores(steps):
    sm = StateManager()
    sm.set_state(
        {
            "case_id": "T2_001",
            "case_type": "harm_assessment",
            "platform_context": "threads",
            "user_profile": {"declared_age": 14},
        },
        "task2_medium",
    )

    for _ in range(steps):
        sm.update_state("restrict", 0.66, False)

    state = sm.get_state()
    assert state["step_number"] == steps
    assert len(state["episode_scores"]) == steps
    assert all(s == 0.66 for s in state["episode_scores"])
