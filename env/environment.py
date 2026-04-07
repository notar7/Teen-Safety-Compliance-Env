"""Main OpenEnv environment used by the project.

It wires task scenarios, graders, state tracking, and reward computation.
"""

import random
from typing import Optional

from env.models import TeenSafetyObservation, TeenSafetyAction, TeenSafetyReward
from env.state_manager import StateManager
from env.reward import RewardCalculator
from tasks.task1_easy import TASK1_SCENARIOS, grade_task1
from tasks.task2_medium import TASK2_SCENARIOS, grade_task2
from tasks.task3_hard import TASK3_SCENARIOS, grade_task3

# Use OpenEnv base class when available; fall back in local/test setups.
try:
    from openenv import BaseEnvironment as _Base
except ImportError:
    class _Base:  # type: ignore
        """Minimal fallback base when openenv-core is not installed."""
        pass


_TASK_REGISTRY = {
    "task1_easy":   (TASK1_SCENARIOS,   grade_task1),
    "task2_medium": (TASK2_SCENARIOS,   grade_task2),
    "task3_hard":   (TASK3_SCENARIOS,   grade_task3),
}

_TASK_INSTRUCTIONS = {
    "task1_easy": (
        "Review this content and decide if it is appropriate for a teenage user. "
        "Choose from: allow, restrict, block, escalate. "
        "Also specify if a warning label or other additional action should be applied."
    ),
    "task2_medium": (
        "Assess if this content poses psychological harm risk to a teenage user. "
        "Consider subtle harms such as unhealthy body image, dangerous viral trends, "
        "financial scams, manipulative influencers, or mental health misinformation. "
        "Choose from: allow, restrict, block, escalate."
    ),
    "task3_hard": (
        "Analyze the behavioral signals for this account and determine if the user has "
        "misrepresented their age to access adult features. You have NO direct age proof — "
        "use behavioral patterns to make your decision. "
        "Choose from: allow, restrict, block, escalate, request_verification."
    ),
}

_VALID_TASK_IDS = set(_TASK_REGISTRY.keys())


class TeenSafetyEnvironment(_Base):
    """
    OpenEnv-compliant Teen Safety Compliance environment.

    The agent plays the role of Meta's automated Teen Safety Compliance system.
    It receives cases — content, accounts, or features — and must make safety
    decisions to protect teenage users across Instagram, Facebook, and Threads.

    Episode flow:
        obs = env.reset(task_id="task1_easy")
        while not done:
            action = agent.decide(obs)
            obs, reward, done, info = env.step(action)

    Attributes:
        MAX_STEPS (int): Maximum steps per episode before auto-termination (default 5)
        rng_seed  (int | None): Optional seed for reproducibility
    """

    MAX_STEPS: int = 5

    def __init__(self, rng_seed: Optional[int] = None):
        self._state_manager = StateManager()
        self._reward_calculator = RewardCalculator()

        self._current_task_id: Optional[str] = None
        self._current_scenario: Optional[dict] = None
        self._step_count: int = 0
        self._episode_reward: float = 0.0
        self._previous_actions: list[str] = []

        # Seeded RNG for reproducible scenario selection.
        self._rng = random.Random(rng_seed)

    def reset(self, task_id: str = "task1_easy") -> TeenSafetyObservation:
        """
        Reset the environment and return the first observation.

        Args:
            task_id (str): Which task to run. One of:
                           'task1_easy' | 'task2_medium' | 'task3_hard'

        Returns:
            TeenSafetyObservation: Initial observation for the episode

        Raises:
            ValueError: If task_id is not recognized
        """
        if task_id not in _VALID_TASK_IDS:
            raise ValueError(
                f"Unknown task_id '{task_id}'. "
                f"Valid options: {sorted(_VALID_TASK_IDS)}"
            )

        # Reset episode state.
        self._current_task_id = task_id
        self._step_count = 0
        self._episode_reward = 0.0
        self._previous_actions = []

        # Pick one scenario for this episode.
        scenarios, _ = _TASK_REGISTRY[task_id]
        self._current_scenario = self._rng.choice(scenarios)

        # Initialize shared state snapshot.
        self._state_manager.set_state(self._current_scenario, task_id)

        return self._build_observation()

    def step(
        self, action: TeenSafetyAction
    ) -> tuple[TeenSafetyObservation, TeenSafetyReward, bool, dict]:
        """
        Process the agent's action and advance the episode.

        Args:
            action (TeenSafetyAction): The agent's compliance decision

        Returns:
            tuple:
                - TeenSafetyObservation : updated observation
                - TeenSafetyReward      : reward with score, breakdown, feedback
                - bool                  : done flag (True = episode finished)
                - dict                  : info dict with episode_reward, step_count

        Raises:
            RuntimeError: If called before reset()
        """
        if self._current_scenario is None:
            raise RuntimeError("Call reset() before step().")

        self._step_count += 1

        _, grader = _TASK_REGISTRY[self._current_task_id]
        ground_truth = self._current_scenario["ground_truth"]

        action_dict = action.model_dump()
        raw_score = grader(action_dict, ground_truth)

        reward = self._reward_calculator.compute(
            score=raw_score,
            action=action_dict,
            ground_truth=ground_truth,
            task_id=self._current_task_id,
        )

        self._episode_reward += reward.score
        # Keep all exposed score-like values strictly within (0, 1) for validator compatibility.
        self._episode_reward = min(max(self._episode_reward, 0.01), 0.99)
        self._previous_actions.append(str(action.decision))

        # Stop when max steps are reached or score is already strong.
        done = (self._step_count >= self.MAX_STEPS) or (reward.score >= 0.80)

        self._state_manager.update_state(
            action_decision=action.decision,
            step_score=reward.score,
            done=done,
        )

        info = {
            "episode_reward": round(self._episode_reward, 4),
            "step_count": self._step_count,
            "done": done,
            "task_id": self._current_task_id,
            "case_id": self._current_scenario["case_id"],
        }

        return self._build_observation(), reward, done, info

    def state(self) -> dict:
        """
        Return the current full episode state.
        Called by GET /state in the FastAPI server.

        Returns:
            dict: Current episode state from StateManager
        """
        return self._state_manager.get_state()

    def _build_observation(self) -> TeenSafetyObservation:
        """Construct a TeenSafetyObservation from current state."""
        s = self._current_scenario
        return TeenSafetyObservation(
            case_id=s["case_id"],
            case_type=s["case_type"],
            content=s["content"],
            user_profile=s["user_profile"],
            platform_context=s["platform_context"],
            previous_actions=list(self._previous_actions),
            step_number=self._step_count,
            task_id=self._current_task_id,
            instructions=_TASK_INSTRUCTIONS[self._current_task_id],
        )
