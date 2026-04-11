"""Task 9 (hard): adversarial mixed-signal moderation with counterfactual checks."""

TASK9_SCENARIOS = [
    {
        "case_id": "T9_001",
        "case_type": "advanced_harm_assessment",
        "content": {
            "content_type": "video",
            "caption": "Awareness only: never try this challenge.",
            "subtitle_text": "step-by-step how to bypass safety locks",
            "hashtags": ["#awareness", "#h4ck", "#teenchallenge"],
            "comments_sample": ["this bypass works", "doing this tonight"],
        },
        "user_profile": {
            "declared_age": 16,
            "interests": ["tech", "challenges"],
            "account_age_days": 260,
        },
        "platform_context": "instagram",
        "ground_truth": {
            "correct_decision": "restrict",
            "acceptable_decisions": ["restrict", "block", "escalate"],
            "key_signals": [
                "awareness framing",
                "step-by-step",
                "bypass",
                "mixed signals",
                "teen challenge",
            ],
            "confidence_band": [0.45, 0.82],
            "explanation": "Content claims awareness but operationally teaches risky bypass behavior; requires hard moderation judgment.",
        },
    },
    {
        "case_id": "T9_002",
        "case_type": "advanced_harm_assessment",
        "content": {
            "content_type": "post",
            "caption": "Study productivity routine",
            "body_text": "microdose stimulants before exams; teachers never notice",
            "hashtags": ["#studytok", "#grind", "#focus"],
            "monetized_link": "boost-pills.example",
        },
        "user_profile": {
            "declared_age": 17,
            "interests": ["academics", "productivity"],
            "account_age_days": 500,
        },
        "platform_context": "threads",
        "ground_truth": {
            "correct_decision": "block",
            "acceptable_decisions": ["block", "restrict", "escalate"],
            "key_signals": [
                "stimulants",
                "exam pressure",
                "monetized link",
                "unsafe advice",
            ],
            "confidence_band": [0.5, 0.9],
            "explanation": "Substance misuse instruction targeting teens in exam context should be blocked or tightly restricted.",
        },
    },
]


def grade_task9(action: dict, ground_truth: dict) -> float:
    """Deterministic hard-task grader emphasizing evidence and confidence calibration."""
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
    if reason and any(sig in reason for sig in key_signals):
        score += 0.20

    try:
        confidence = float(action.get("confidence", 0.0))
    except (TypeError, ValueError):
        confidence = 0.0

    low, high = ground_truth.get("confidence_band", [0.45, 0.85])
    if float(low) <= confidence <= float(high):
        score += 0.12

    if len(reason) > 30:
        score += 0.17

    return round(min(max(score, 0.01), 0.99), 2)
