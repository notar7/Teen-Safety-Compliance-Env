import pytest

from tasks.task1_easy import TASK1_SCENARIOS, grade_task1
from tasks.task2_medium import TASK2_SCENARIOS, grade_task2
from tasks.task3_hard import TASK3_SCENARIOS, grade_task3


@pytest.mark.parametrize("scenario", TASK1_SCENARIOS)
def test_task1_all_scenarios_correct_action_scores_high(scenario):
    gt = scenario["ground_truth"]
    action = {
        "decision": gt["correct_decision"],
        "confidence": max(float(gt.get("minimum_confidence", 0.8)), 0.85),
        "reason": "This content is unsafe for minors and violates teen safety policy, so we must enforce the strict control.",
        "additional_action": gt.get("correct_additional_action"),
    }
    score = grade_task1(action, gt)
    assert score >= 0.85


@pytest.mark.parametrize("scenario", TASK2_SCENARIOS)
def test_task2_all_scenarios_correct_action_scores_high(scenario):
    gt = scenario["ground_truth"]
    expected_keywords = gt.get("expected_keywords", [])
    keyword = expected_keywords[0] if expected_keywords else "harm"

    action = {
        "decision": gt["correct_decision"],
        "confidence": 0.7,
        "reason": f"This may cause {keyword} risk for teenagers and needs protection.",
        "additional_action": "add_warning_label" if gt.get("requires_label") else None,
    }
    score = grade_task2(action, gt)
    assert score >= 0.8


@pytest.mark.parametrize("scenario", TASK3_SCENARIOS)
def test_task3_all_scenarios_correct_action_scores_high(scenario):
    gt = scenario["ground_truth"]
    key_signals = gt.get("key_signals", [])
    # Include up to first 3 key signals to maximize evidence scoring in grader
    evidence = ", ".join(key_signals[:3]) if key_signals else "behavioral signals"

    action = {
        "decision": gt["correct_decision"],
        "confidence": min(float(gt.get("max_expected_confidence", 0.75)), 0.7),
        "reason": f"Request age verification due to {evidence}.",
        "additional_action": None,
    }
    score = grade_task3(action, gt)
    assert score >= 0.8
