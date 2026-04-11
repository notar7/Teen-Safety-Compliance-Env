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
from tasks.task4_easy import TASK4_SCENARIOS, grade_task4
from tasks.task5_easy import TASK5_SCENARIOS, grade_task5
from tasks.task6_medium import TASK6_SCENARIOS, grade_task6
from tasks.task7_medium import TASK7_SCENARIOS, grade_task7
from tasks.task8_medium import TASK8_SCENARIOS, grade_task8
from tasks.task9_hard import TASK9_SCENARIOS, grade_task9
from tasks.task10_hard import TASK10_SCENARIOS, grade_task10

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
    "task4_easy":   (TASK4_SCENARIOS,   grade_task4),
    "task5_easy":   (TASK5_SCENARIOS,   grade_task5),
    "task6_medium": (TASK6_SCENARIOS,   grade_task6),
    "task7_medium": (TASK7_SCENARIOS,   grade_task7),
    "task8_medium": (TASK8_SCENARIOS,   grade_task8),
    "task9_hard":   (TASK9_SCENARIOS,   grade_task9),
    "task10_hard":  (TASK10_SCENARIOS,  grade_task10),
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
    "task4_easy": (
        "Review obvious dangerous self-harm or violence challenge content for teens. "
        "Choose from: allow, restrict, block, escalate."
    ),
    "task5_easy": (
        "Review obvious sexual exploitation, grooming-adjacent, or adult solicitation content "
        "for under-18 users. Choose from: allow, restrict, block, escalate, request_verification."
    ),
    "task6_medium": (
        "Assess borderline harmful content for teen recommendation surfaces. "
        "Use calibrated moderation and note no-recommend handling in reasoning."
    ),
    "task7_medium": (
        "Assess conflicting metadata/signals where declared safe context may hide harmful intent. "
        "Choose from: allow, restrict, block, escalate."
    ),
    "task8_medium": (
        "Assess teen privacy/location exposure risk and potential exploitation pathways. "
        "Choose from: allow, restrict, block, escalate."
    ),
    "task9_hard": (
        "Handle adversarial mixed-signal cases. Apply careful uncertainty-aware moderation "
        "with explainable evidence."
    ),
    "task10_hard": (
        "Detect obfuscated/coded harmful intent targeting teens. "
        "Choose from: allow, restrict, block, escalate."
    ),
}

_TASK_METADATA = {
    "task1_easy": {
        "id": "task1_easy",
        "name": "Obvious Content Restriction",
        "difficulty": "easy",
        "description": "Detect and block obviously inappropriate content for teen users",
        "expected_score_range": "0.70 - 0.99",
    },
    "task2_medium": {
        "id": "task2_medium",
        "name": "Subtle Harm Assessment",
        "difficulty": "medium",
        "description": "Assess subtle psychological harm in content targeting teenagers",
        "expected_score_range": "0.40 - 0.90",
    },
    "task3_hard": {
        "id": "task3_hard",
        "name": "Age Misrepresentation Detection",
        "difficulty": "hard",
        "description": "Detect age fraud from behavioral signals alone",
        "expected_score_range": "0.20 - 0.80",
    },
    "task4_easy": {
        "id": "task4_easy",
        "name": "Obvious Self-Harm Suppression",
        "difficulty": "easy",
        "description": "Block direct self-harm and violence challenge content for minors",
        "expected_score_range": "0.70 - 0.99",
    },
    "task5_easy": {
        "id": "task5_easy",
        "name": "Grooming and Exploitation Blocking",
        "difficulty": "easy",
        "description": "Block overt grooming-adjacent and adult solicitation content",
        "expected_score_range": "0.70 - 0.99",
    },
    "task6_medium": {
        "id": "task6_medium",
        "name": "Recommendation Risk Gating",
        "difficulty": "medium",
        "description": "Moderate borderline harmful content and enforce no-recommend safety",
        "expected_score_range": "0.45 - 0.95",
    },
    "task7_medium": {
        "id": "task7_medium",
        "name": "Conflicting Signal Resolution",
        "difficulty": "medium",
        "description": "Handle ambiguity where safe framing conflicts with risky metadata",
        "expected_score_range": "0.45 - 0.95",
    },
    "task8_medium": {
        "id": "task8_medium",
        "name": "Teen Privacy Exposure Control",
        "difficulty": "medium",
        "description": "Restrict privacy/location-exposure patterns targeting minors",
        "expected_score_range": "0.45 - 0.95",
    },
    "task9_hard": {
        "id": "task9_hard",
        "name": "Adversarial Mixed-Signal Moderation",
        "difficulty": "hard",
        "description": "Adjudicate hard contradictory safety cases with calibrated confidence",
        "expected_score_range": "0.35 - 0.95",
    },
    "task10_hard": {
        "id": "task10_hard",
        "name": "Obfuscated Harm Detection",
        "difficulty": "hard",
        "description": "Decode coded harmful language targeting teen audiences",
        "expected_score_range": "0.35 - 0.95",
    },
}

_VALID_TASK_IDS = set(_TASK_REGISTRY.keys())

_RISK_MARKERS = {
    "critical": ["adult_content", "porn", "casino", "gambling", "firearm", "weapons", "vape", "nicotine"],
    "high": ["starvation", "72-hour fast", "depression", "stop taking meds", "scam", "mlm", "cyberbullying", "grooming"],
    "subtle": ["body image", "thinspiration", "peer pressure", "unverified", "class of", "school"],
    "adversarial": ["v@pe", "c@sino", "pr0n", "g4mbl", "sk00l", "fr3shers"],
}


def get_task_ids() -> list[str]:
    """Return stable ordered task ids."""
    return list(_TASK_REGISTRY.keys())


def get_task_catalog() -> list[dict]:
    """Return task metadata list including scenario counts."""
    catalog: list[dict] = []
    for task_id in get_task_ids():
        meta = dict(_TASK_METADATA[task_id])
        meta["num_scenarios"] = len(_TASK_REGISTRY[task_id][0])
        catalog.append(meta)
    return catalog


def _flatten_text(value) -> list[str]:
    out: list[str] = []
    if isinstance(value, dict):
        for v in value.values():
            out.extend(_flatten_text(v))
    elif isinstance(value, list):
        for v in value:
            out.extend(_flatten_text(v))
    elif isinstance(value, str):
        text = value.strip().lower()
        if text:
            out.append(text)
    return out


def _build_policy_trace(task_id: str, scenario: dict, action: dict, ground_truth: dict) -> dict:
    """Build deterministic signal -> rule -> action trace for auditability."""
    flattened = " | ".join(_flatten_text(scenario.get("content", {})))

    marker_hits = {
        key: [m for m in markers if m in flattened][:5]
        for key, markers in _RISK_MARKERS.items()
    }

    risk_tier = "low"
    if marker_hits["critical"] or marker_hits["adversarial"]:
        risk_tier = "critical"
    elif marker_hits["high"]:
        risk_tier = "high"
    elif marker_hits["subtle"]:
        risk_tier = "subtle"

    decision = str(action.get("decision", "")).strip().lower()
    correct = str(ground_truth.get("correct_decision", "")).strip().lower()
    acceptable = [str(v).strip().lower() for v in ground_truth.get("acceptable_decisions", [])]

    if decision == correct:
        decision_alignment = "correct"
    elif decision in acceptable:
        decision_alignment = "acceptable"
    else:
        decision_alignment = "mismatch"

    evidence = marker_hits["critical"] + marker_hits["high"] + marker_hits["subtle"] + marker_hits["adversarial"]
    evidence = evidence[:8]

    return {
        "task_id": task_id,
        "risk_tier": risk_tier,
        "signals": evidence,
        "rule_triggered": f"{task_id}:{risk_tier}",
        "decision": decision,
        "decision_alignment": decision_alignment,
        "counterfactual": "if user were older, allow/restrict threshold may relax" if risk_tier in {"critical", "high"} else "no counterfactual escalation",
        "recommendation_gate": (
            "block_all_surfaces" if risk_tier == "critical"
            else "restrict_no_recommend" if risk_tier == "high"
            else "allow_with_warning_no_discovery_boost" if risk_tier == "subtle"
            else "allow"
        ),
    }


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
        policy_trace = _build_policy_trace(
            task_id=self._current_task_id,
            scenario=self._current_scenario,
            action=action_dict,
            ground_truth=ground_truth,
        )

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
            policy_trace=policy_trace,
        )

        info = {
            "episode_reward": round(self._episode_reward, 4),
            "step_count": self._step_count,
            "done": done,
            "task_id": self._current_task_id,
            "case_id": self._current_scenario["case_id"],
            "policy_trace": policy_trace,
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
