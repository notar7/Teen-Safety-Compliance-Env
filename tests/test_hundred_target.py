from tasks.task1_easy import TASK1_SCENARIOS, grade_task1
from tasks.task2_medium import TASK2_SCENARIOS, grade_task2
from tasks.task3_hard import TASK3_SCENARIOS, grade_task3


def _idx(case_id: str) -> int:
    return int(case_id.split("_")[1]) - 1


def _best_action_task1(gt: dict) -> dict:
    return {
        "decision": gt["correct_decision"],
        "confidence": max(float(gt.get("minimum_confidence", 0.8)), 0.9),
        "reason": "This content is unsafe for minors and violates teen safety policy, so it must be restricted.",
        "additional_action": gt.get("correct_additional_action"),
    }


def _best_action_task2(gt: dict) -> dict:
    kws = gt.get("expected_keywords", ["harm"])
    return {
        "decision": gt["correct_decision"],
        "confidence": 0.7,
        "reason": f"Potential {kws[0]} risk for teens; this can cause psychological harm.",
        "additional_action": "add_warning_label" if gt.get("requires_label") else None,
    }


def _best_action_task3(gt: dict) -> dict:
    signals = ", ".join(gt.get("key_signals", [])[:3]) or "behavioral signals"
    return {
        "decision": gt["correct_decision"],
        "confidence": min(float(gt.get("max_expected_confidence", 0.75)), 0.7),
        "reason": f"Request age verification due to {signals}.",
        "additional_action": None,
    }


def test_task1_case_001():
    s = TASK1_SCENARIOS[_idx("T1_001")]
    assert grade_task1(_best_action_task1(s["ground_truth"]), s["ground_truth"]) >= 0.85


def test_task1_case_002():
    s = TASK1_SCENARIOS[_idx("T1_002")]
    assert grade_task1(_best_action_task1(s["ground_truth"]), s["ground_truth"]) >= 0.85


def test_task1_case_003():
    s = TASK1_SCENARIOS[_idx("T1_003")]
    assert grade_task1(_best_action_task1(s["ground_truth"]), s["ground_truth"]) >= 0.85


def test_task1_case_004():
    s = TASK1_SCENARIOS[_idx("T1_004")]
    assert grade_task1(_best_action_task1(s["ground_truth"]), s["ground_truth"]) >= 0.85


def test_task1_case_005():
    s = TASK1_SCENARIOS[_idx("T1_005")]
    assert grade_task1(_best_action_task1(s["ground_truth"]), s["ground_truth"]) >= 0.85


def test_task1_case_006():
    s = TASK1_SCENARIOS[_idx("T1_006")]
    assert grade_task1(_best_action_task1(s["ground_truth"]), s["ground_truth"]) >= 0.85


def test_task2_case_001():
    s = TASK2_SCENARIOS[_idx("T2_001")]
    assert grade_task2(_best_action_task2(s["ground_truth"]), s["ground_truth"]) >= 0.8


def test_task2_case_002():
    s = TASK2_SCENARIOS[_idx("T2_002")]
    assert grade_task2(_best_action_task2(s["ground_truth"]), s["ground_truth"]) >= 0.8


def test_task2_case_003():
    s = TASK2_SCENARIOS[_idx("T2_003")]
    assert grade_task2(_best_action_task2(s["ground_truth"]), s["ground_truth"]) >= 0.8


def test_task2_case_004():
    s = TASK2_SCENARIOS[_idx("T2_004")]
    assert grade_task2(_best_action_task2(s["ground_truth"]), s["ground_truth"]) >= 0.8


def test_task2_case_005():
    s = TASK2_SCENARIOS[_idx("T2_005")]
    assert grade_task2(_best_action_task2(s["ground_truth"]), s["ground_truth"]) >= 0.8


def test_task2_case_006():
    s = TASK2_SCENARIOS[_idx("T2_006")]
    assert grade_task2(_best_action_task2(s["ground_truth"]), s["ground_truth"]) >= 0.8


def test_task3_case_001():
    s = TASK3_SCENARIOS[_idx("T3_001")]
    assert grade_task3(_best_action_task3(s["ground_truth"]), s["ground_truth"]) >= 0.8


def test_task3_case_002():
    s = TASK3_SCENARIOS[_idx("T3_002")]
    assert grade_task3(_best_action_task3(s["ground_truth"]), s["ground_truth"]) >= 0.8


def test_task3_case_003():
    s = TASK3_SCENARIOS[_idx("T3_003")]
    assert grade_task3(_best_action_task3(s["ground_truth"]), s["ground_truth"]) >= 0.8


def test_task3_case_004():
    s = TASK3_SCENARIOS[_idx("T3_004")]
    assert grade_task3(_best_action_task3(s["ground_truth"]), s["ground_truth"]) >= 0.8


def test_task3_case_005():
    s = TASK3_SCENARIOS[_idx("T3_005")]
    assert grade_task3(_best_action_task3(s["ground_truth"]), s["ground_truth"]) >= 0.8


def test_task3_case_006():
    s = TASK3_SCENARIOS[_idx("T3_006")]
    assert grade_task3(_best_action_task3(s["ground_truth"]), s["ground_truth"]) >= 0.8
