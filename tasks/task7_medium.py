"""Task 7 (medium): conflicting metadata and ambiguous safety context."""

from tasks.task2_medium import grade_task2


TASK7_SCENARIOS = [
    {
        "case_id": "T7_001",
        "case_type": "harm_assessment",
        "content": {
            "content_type": "educational_video",
            "caption": "Safety awareness: why gambling addiction destroys families.",
            "image_tags": ["casino", "jackpot", "teenwins"],
            "comments_sample": ["where to play?", "best casino app?"],
            "monetization_links": ["spin-big-now.example"],
        },
        "user_profile": {
            "declared_age": 14,
            "interests": ["gaming", "finance"],
            "account_age_days": 200,
        },
        "platform_context": "facebook",
        "ground_truth": {
            "correct_decision": "escalate",
            "acceptable_decisions": ["escalate", "restrict"],
            "requires_label": True,
            "expected_keywords": [
                "conflicting signals",
                "metadata",
                "gambling",
                "uncertain",
                "review",
            ],
            "explanation": "Educational framing conflicts with promotion-like signals and risky links; escalate for review.",
        },
    },
    {
        "case_id": "T7_002",
        "case_type": "harm_assessment",
        "content": {
            "content_type": "livestream_clip",
            "caption": "anti-bullying campaign",
            "subtitle_text": "let's roast losers in comments",
            "engagement_prompt": "tag the ugliest classmate",
            "creator_type": "school_creator",
        },
        "user_profile": {
            "declared_age": 13,
            "interests": ["school", "memes"],
            "account_age_days": 140,
        },
        "platform_context": "instagram",
        "ground_truth": {
            "correct_decision": "restrict",
            "acceptable_decisions": ["restrict", "escalate"],
            "requires_label": True,
            "expected_keywords": [
                "cyberbullying",
                "harassment",
                "conflict",
                "safety",
                "warning",
            ],
            "explanation": "Declared anti-bullying context conflicts with explicit harassment cueing; restrict and warn.",
        },
    },
]


def grade_task7(action: dict, ground_truth: dict) -> float:
    """Reuse medium-task deterministic grading."""
    return grade_task2(action, ground_truth)
