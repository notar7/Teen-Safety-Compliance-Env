from tasks.task1_easy import TASK1_SCENARIOS, grade_task1
from tasks.task2_medium import TASK2_SCENARIOS, grade_task2
from tasks.task3_hard import TASK3_SCENARIOS, grade_task3


def test_task1_grader_rewards_correct_more_than_wrong():
    gt = TASK1_SCENARIOS[0]["ground_truth"]
    correct = grade_task1(
        {"decision": gt["correct_decision"], "confidence": 0.95, "reason": "This is clearly unsafe for minors and should be blocked immediately.", "additional_action": "add_warning_label"},
        gt,
    )
    wrong = grade_task1(
        {"decision": "allow", "confidence": 0.2, "reason": "ok", "additional_action": None},
        gt,
    )
    assert correct > wrong


def test_task2_grader_warning_and_keywords_help():
    gt = TASK2_SCENARIOS[0]["ground_truth"]
    strong = grade_task2(
        {"decision": "restrict", "confidence": 0.7, "reason": "This promotes a dangerous diet with 500 calories and body image harm.", "additional_action": "add_warning_label"},
        gt,
    )
    weak = grade_task2(
        {"decision": "allow", "confidence": 0.99, "reason": "fine", "additional_action": None},
        gt,
    )
    assert strong > weak


def test_task3_grader_signal_mentions_help():
    gt = TASK3_SCENARIOS[0]["ground_truth"]
    strong = grade_task3(
        {
            "decision": "request_verification",
            "confidence": 0.6,
            "reason": "Need age verification due to class of 2027, high school, and school library signals.",
            "additional_action": None,
        },
        gt,
    )
    weak = grade_task3(
        {"decision": "allow", "confidence": 0.99, "reason": "looks adult", "additional_action": None},
        gt,
    )
    assert strong > weak
