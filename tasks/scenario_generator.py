"""Helpers for sampling and looking up task scenarios."""

import random
from typing import Literal

from tasks.task1_easy import TASK1_SCENARIOS
from tasks.task2_medium import TASK2_SCENARIOS
from tasks.task3_hard import TASK3_SCENARIOS

_ALL_SCENARIOS = {
    "task1_easy":   TASK1_SCENARIOS,
    "task2_medium": TASK2_SCENARIOS,
    "task3_hard":   TASK3_SCENARIOS,
}

TaskId = Literal["task1_easy", "task2_medium", "task3_hard"]


def get_scenario(task_id: TaskId, rng: random.Random | None = None) -> dict:
    """
    Return a random scenario for the given task.

    Args:
        task_id (str): One of 'task1_easy', 'task2_medium', 'task3_hard'
        rng (random.Random | None): Optional seeded RNG for reproducibility.
                                    Uses global random if not provided.

    Returns:
        dict: A single scenario dict with case_id, content, user_profile,
              platform_context, and ground_truth.

    Raises:
        ValueError: If task_id is not recognized.
    """
    if task_id not in _ALL_SCENARIOS:
        raise ValueError(
            f"Unknown task_id '{task_id}'. "
            f"Valid: {list(_ALL_SCENARIOS.keys())}"
        )
    pool = _ALL_SCENARIOS[task_id]
    chooser = rng if rng is not None else random
    return chooser.choice(pool)


def get_all_scenarios(task_id: TaskId) -> list[dict]:
    """
    Return all scenarios for the given task.

    Args:
        task_id (str): One of 'task1_easy', 'task2_medium', 'task3_hard'

    Returns:
        list[dict]: All scenario dicts for the task
    """
    if task_id not in _ALL_SCENARIOS:
        raise ValueError(f"Unknown task_id '{task_id}'.")
    return list(_ALL_SCENARIOS[task_id])


def get_scenario_by_id(case_id: str) -> dict | None:
    """
    Find a scenario by its case_id across all tasks.

    Args:
        case_id (str): e.g. 'T1_003', 'T2_007', 'T3_002'

    Returns:
        dict | None: The scenario dict, or None if not found
    """
    for scenarios in _ALL_SCENARIOS.values():
        for s in scenarios:
            if s["case_id"] == case_id:
                return s
    return None


def scenario_counts() -> dict:
    """Return number of scenarios per task."""
    return {task_id: len(s) for task_id, s in _ALL_SCENARIOS.items()}
