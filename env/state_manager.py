"""
env/state_manager.py
--------------------
Manages the current state of the TeenSafetyEnvironment episode.
Stores scenario, task, step history, and provides a clean state dict.
"""


class StateManager:
    """
    Tracks the full state of an active episode.
    Returned by env.state() — inspectable by agents and servers.
    """

    def __init__(self):
        self._state: dict = {}

    def set_state(self, scenario: dict, task_id: str) -> None:
        """
        Initialize state from a fresh scenario at episode start.

        Args:
            scenario (dict): The current scenario being evaluated
            task_id  (str):  Which task is running (task1_easy / task2_medium / task3_hard)
        """
        self._state = {
            "task_id": task_id,
            "case_id": scenario.get("case_id", ""),
            "case_type": scenario.get("case_type", ""),
            "platform_context": scenario.get("platform_context", ""),
            "user_profile": scenario.get("user_profile", {}),
            "step_number": 0,
            "previous_actions": [],
            "episode_scores": [],
            "episode_done": False,
        }

    def update_state(self, action_decision: str, step_score: float, done: bool) -> None:
        """
        Update state after each step.

        Args:
            action_decision (str):  The decision the agent made this step
            step_score      (float): Score awarded for this step
            done            (bool):  Whether the episode is finished
        """
        self._state["step_number"] += 1
        self._state["previous_actions"].append(action_decision)
        self._state["episode_scores"].append(round(step_score, 4))
        self._state["episode_done"] = done

    def get_state(self) -> dict:
        """
        Return a copy of the current state dict (safe to expose via API).

        Returns:
            dict: Full episode state
        """
        return dict(self._state)

    def reset(self) -> None:
        """Clear all state (called internally before set_state)."""
        self._state = {}
