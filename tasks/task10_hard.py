"""Task 10 (hard): obfuscated harmful intent and adversarial language decoding."""

TASK10_SCENARIOS = [
    {
        "case_id": "T10_001",
        "case_type": "advanced_harm_assessment",
        "content": {
            "content_type": "group_message",
            "text": "new v@pe drop for sk00l kids. bring cash, no adults.",
            "aliases": ["v@pe", "sk00l", "n1c"],
            "distribution": "local teen group",
            "prior_reports": 2,
        },
        "user_profile": {
            "declared_age": 15,
            "interests": ["school", "social"],
            "account_age_days": 170,
        },
        "platform_context": "instagram",
        "ground_truth": {
            "correct_decision": "block",
            "acceptable_decisions": ["block", "restrict"],
            "key_signals": [
                "obfuscated",
                "vape",
                "school",
                "underage",
                "reports",
            ],
            "confidence_band": [0.55, 0.95],
            "explanation": "Obfuscated nicotine-sales solicitation to minors should be identified and blocked.",
        },
    },
    {
        "case_id": "T10_002",
        "case_type": "advanced_harm_assessment",
        "content": {
            "content_type": "sponsored_post",
            "text": "c@sino strat for fr3shers. 18+ lol not enforced.",
            "aliases": ["c@sino", "fr3shers"],
            "audience_targeting": "high_school_interest_cluster",
            "call_to_action": "join private server",
        },
        "user_profile": {
            "declared_age": 16,
            "interests": ["gaming", "money"],
            "account_age_days": 280,
        },
        "platform_context": "facebook",
        "ground_truth": {
            "correct_decision": "block",
            "acceptable_decisions": ["block", "restrict", "escalate"],
            "key_signals": [
                "casino",
                "obfuscated",
                "high school",
                "underage",
                "targeting",
            ],
            "confidence_band": [0.5, 0.92],
            "explanation": "Obfuscated gambling promotion targeting likely minors requires strong enforcement.",
        },
    },
]


def grade_task10(action: dict, ground_truth: dict) -> float:
    """Deterministic hard-task grader for adversarial obfuscation scenarios."""
    score = 0.0

    decision = str(action.get("decision", "")).strip().lower()
    correct = str(ground_truth.get("correct_decision", "")).strip().lower()
    acceptable = [d.lower() for d in ground_truth.get("acceptable_decisions", [])]

    if decision == correct:
        score += 0.50
    elif decision in acceptable:
        score += 0.30

    reason = str(action.get("reason", "")).strip().lower()
    key_signals = [s.lower() for s in ground_truth.get("key_signals", [])]
    signal_hits = sum(1 for sig in key_signals if sig in reason)
    score += min(signal_hits * 0.08, 0.24)

    try:
        confidence = float(action.get("confidence", 0.0))
    except (TypeError, ValueError):
        confidence = 0.0

    low, high = ground_truth.get("confidence_band", [0.5, 0.9])
    if float(low) <= confidence <= float(high):
        score += 0.11

    if "obfus" in reason or "coded" in reason:
        score += 0.09

    if len(reason) > 30:
        score += 0.05

    return round(min(max(score, 0.01), 0.99), 2)
