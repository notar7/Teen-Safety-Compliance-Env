from env.reward import RewardCalculator


def test_reward_calculator_clamps_and_builds_feedback():
    rc = RewardCalculator()
    reward = rc.compute(
        score=1.5,
        action={"decision": "block", "confidence": 0.95, "reason": "good reason", "additional_action": None},
        ground_truth={"correct_decision": "block", "acceptable_decisions": ["restrict"], "explanation": "because policy"},
        task_id="task1_easy",
    )

    assert reward.score == 0.99
    assert reward.breakdown["decision_match"] == "correct"
    assert isinstance(reward.feedback, str) and len(reward.feedback) > 0
