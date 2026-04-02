import pytest
from pydantic import ValidationError

from env.models import TeenSafetyAction, TeenSafetyObservation, TeenSafetyReward


def test_models_happy_path():
    obs = TeenSafetyObservation(
        case_id="X1",
        case_type="content_review",
        content={"text": "hello"},
        user_profile={"declared_age": 15},
        platform_context="instagram",
        step_number=0,
        task_id="task1_easy",
        instructions="review",
    )
    action = TeenSafetyAction(
        decision="restrict",
        confidence=0.8,
        reason="Potentially harmful for teens.",
        additional_action="add_warning_label",
    )
    reward = TeenSafetyReward(score=0.8, breakdown={"ok": True}, feedback="good")

    assert obs.case_id == "X1"
    assert action.decision == "restrict"
    assert reward.score == 0.8


def test_action_confidence_out_of_range_fails():
    with pytest.raises(ValidationError):
        TeenSafetyAction(
            decision="allow",
            confidence=1.5,
            reason="invalid",
            additional_action=None,
        )
