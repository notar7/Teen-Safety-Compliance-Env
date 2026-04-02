import pytest

from tasks import scenario_generator as sg


def test_scenario_counts_and_getters():
    counts = sg.scenario_counts()
    assert counts["task1_easy"] > 0
    assert counts["task2_medium"] > 0
    assert counts["task3_hard"] > 0

    one = sg.get_scenario("task1_easy")
    assert one["case_id"].startswith("T1_")

    all_t2 = sg.get_all_scenarios("task2_medium")
    assert len(all_t2) == counts["task2_medium"]

    fetched = sg.get_scenario_by_id("T3_001")
    assert fetched is not None
    assert fetched["case_id"] == "T3_001"


def test_invalid_task_raises():
    with pytest.raises(ValueError):
        sg.get_scenario("invalid")  # type: ignore[arg-type]
