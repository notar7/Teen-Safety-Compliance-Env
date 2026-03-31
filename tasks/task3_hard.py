"""
TASK 3 — Hard: Age Misrepresentation Detection
-----------------------------------------------
STUB — This file will be fully implemented in Phase 5 (Riyanshi Verma).

Agent must detect when a user has lied about their age to access adult features.
No direct age proof available — agent must reason from behavioral signals only.

6 scenarios varying in signal strength:
  - 2 strong behavioral signals
  - 2 medium mixed signals
  - 2 subtle weak signals

Grader: grade_task3(action, ground_truth) -> float [0.0, 1.0]
"""

# ── Placeholder scenarios (Phase 5 will replace these with 6 full ones) ──

TASK3_SCENARIOS = [
    {
        "case_id": "T3_001",
        "case_type": "age_verification",
        "content": {
            "account_info": {
                "declared_age": 22,
                "account_created": "2023-01-15",
                "profile_bio": "just vibing 😊"
            },
            "behavioral_signals": {
                "posting_times": ["3pm", "4pm", "8pm", "weekends_heavy"],
                "content_interests": ["minecraft", "roblox", "school_memes", "teen_drama_shows"],
                "language_patterns": ["no cap", "bussin", "slay", "periodt", "its giving"],
                "engagement_patterns": "high engagement with teen content creators",
                "reported_by_peers": 3,
                "follows_teen_influencers": True,
                "group_memberships": ["High School Memes", "Class of 2026"],
                "location_tags": [],
            },
            "requested_feature": "access_to_adult_dating_features"
        },
        "user_profile": {
            "declared_age": 22,
            "account_verified": False,
            "account_age_days": 365
        },
        "platform_context": "instagram",
        "ground_truth": {
            "correct_decision": "request_verification",
            "acceptable_decisions": ["request_verification", "restrict"],
            "key_signals": [
                "school memes", "class of 2026", "roblox", "minecraft",
                "posting times", "teen influencers", "reported by peers"
            ],
            "max_expected_confidence": 0.75,
            "explanation": (
                "Strong teen behavioral signals: school-hour posting, teen-only content (Roblox, Minecraft, "
                "school memes), Class of 2026 group membership, 3 peer reports of underage status. "
                "Must request verification before granting adult dating features."
            )
        }
    },
    # Phases 5 will add T3_002 through T3_006
]


def grade_task3(action: dict, ground_truth: dict) -> float:
    """
    Grade an agent's action on Task 3 (Hard) scenarios.
    STUB — will be expanded in Phase 5 with full 6-scenario grader logic.

    Scoring:
        +0.40  → Correct decision (request_verification or restrict)
        +0.20  → Agent explicitly mentions requesting verification
        +0.30  → Agent cites key signals in reasoning (0.10 per signal, max 3)
        +0.10  → Confidence appropriately humble (<= max_expected_confidence)
        Cap at 1.0

    Args:
        action      (dict): Agent's action with keys: decision, confidence, reason, additional_action
        ground_truth (dict): Correct answer reference from scenario

    Returns:
        float: Score between 0.0 and 1.0 (rounded to 2 decimal places)
    """
    score = 0.0

    # ── Core decision ─────────────────────────────────────────────────────
    agent_decision = str(action.get("decision", "")).strip().lower()
    correct_decision = str(ground_truth.get("correct_decision", "")).strip().lower()
    acceptable = [d.lower() for d in ground_truth.get("acceptable_decisions", [])]

    if agent_decision == correct_decision:
        score += 0.40
    elif agent_decision in acceptable:
        score += 0.25

    # ── Verification mention ──────────────────────────────────────────────
    agent_reason = str(action.get("reason", "")).strip().lower()
    agent_additional = str(action.get("additional_action", "") or "").strip().lower()

    verification_mentioned = (
        "request_verification" in agent_decision
        or "verification" in agent_reason
        or "verify" in agent_reason
        or agent_additional == "request_verification"
    )
    if verification_mentioned:
        score += 0.20

    # ── Evidence-based reasoning (key signals cited) ───────────────────────
    key_signals = [sig.lower() for sig in ground_truth.get("key_signals", [])]
    signals_mentioned = sum(1 for sig in key_signals if sig in agent_reason)
    score += min(signals_mentioned * 0.10, 0.30)

    # ── Calibrated confidence (should NOT be overconfident on hard cases) ──
    try:
        agent_confidence = float(action.get("confidence", 0.0))
    except (TypeError, ValueError):
        agent_confidence = 1.0

    max_confidence = float(ground_truth.get("max_expected_confidence", 0.75))
    if agent_confidence <= max_confidence:
        score += 0.10

    return round(min(score, 1.0), 2)
