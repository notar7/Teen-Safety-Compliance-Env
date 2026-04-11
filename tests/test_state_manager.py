from env.state_manager import StateManager


def test_state_manager_set_update_get_reset():
    sm = StateManager()
    scenario = {
        "case_id": "T1_001",
        "case_type": "content_review",
        "platform_context": "instagram",
        "user_profile": {"declared_age": 14},
    }

    sm.set_state(scenario, "task1_easy")
    state = sm.get_state()
    assert state["task_id"] == "task1_easy"
    assert state["step_number"] == 0

    sm.update_state(
        "block",
        0.9,
        True,
        policy_trace={"rule_triggered": "task1_easy:critical", "risk_tier": "critical"},
    )
    state = sm.get_state()
    assert state["step_number"] == 1
    assert state["previous_actions"] == ["block"]
    assert state["episode_scores"] == [0.9]
    assert state["policy_traces"][0]["risk_tier"] == "critical"
    assert state["episode_done"] is True

    sm.reset()
    assert sm.get_state() == {}
