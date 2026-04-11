"""Task 5 (easy): obvious sexual exploitation and grooming exposure control."""

from tasks.task1_easy import grade_task1


TASK5_SCENARIOS = [
    {
        "case_id": "T5_001",
        "case_type": "content_review",
        "content": {
            "content_type": "dm_promo",
            "text": "Adults-only private chat. Teens welcome if discreet. Send selfies to unlock VIP.",
            "image_tags": ["grooming", "adult_chat", "sexualized"],
            "call_to_action": "Message Now",
        },
        "user_profile": {
            "declared_age": 13,
            "account_verified": False,
            "account_age_days": 80,
        },
        "platform_context": "instagram",
        "ground_truth": {
            "correct_decision": "block",
            "acceptable_decisions": ["block"],
            "correct_additional_action": "age_gate",
            "minimum_confidence": 0.9,
            "explanation": "Sexual solicitation and grooming-adjacent calls to action for minors require immediate block.",
        },
    },
    {
        "case_id": "T5_002",
        "case_type": "content_review",
        "content": {
            "content_type": "advertisement",
            "text": "Find nearby adults tonight. No ID checks. 18+ optional.",
            "image_tags": ["adult_dating", "hookup", "18+"],
            "advertiser_category": "adult_dating_platform",
            "call_to_action": "Join",
        },
        "user_profile": {
            "declared_age": 16,
            "account_verified": False,
            "account_age_days": 190,
        },
        "platform_context": "facebook",
        "ground_truth": {
            "correct_decision": "block",
            "acceptable_decisions": ["block"],
            "correct_additional_action": "age_gate",
            "minimum_confidence": 0.85,
            "explanation": "Adult dating exposure with weak age controls must be blocked for under-18 users.",
        },
    },
]


def grade_task5(action: dict, ground_truth: dict) -> float:
    """Reuse easy-task deterministic grading."""
    return grade_task1(action, ground_truth)
