"""Task 1 (easy): obvious content restrictions for under-18 users."""

TASK1_SCENARIOS = [

    # ── Scenario 1: Alcohol Advertisement ──────────────────────────────────
    {
        "case_id": "T1_001",
        "case_type": "content_review",
        "content": {
            "content_type": "advertisement",
            "text": "Get 20% off your first order of premium whiskey! 🥃 Limited time offer — shop now.",
            "image_tags": ["alcohol", "whiskey_bottle", "adults_only"],
            "advertiser_category": "alcohol_brand",
            "target_audience_set_by_advertiser": "18+",
            "call_to_action": "Shop Now"
        },
        "user_profile": {
            "declared_age": 15,
            "account_verified": False,
            "account_age_days": 120
        },
        "platform_context": "instagram",
        "ground_truth": {
            "correct_decision": "block",
            "acceptable_decisions": ["block", "restrict"],
            "correct_additional_action": "add_warning_label",
            "minimum_confidence": 0.8,
            "explanation": "Alcohol advertising is strictly prohibited from being shown to users under 18. Must be blocked immediately."
        }
    },

    # ── Scenario 2: Gambling Promotion ─────────────────────────────────────
    {
        "case_id": "T1_002",
        "case_type": "content_review",
        "content": {
            "content_type": "sponsored_post",
            "text": "Win BIG tonight! 💰 Join our online casino and get a $500 welcome bonus. 18+ only.",
            "image_tags": ["casino", "money", "gambling", "jackpot"],
            "link_domain": "spinpalace-casino.com",
            "advertiser_category": "gambling",
            "call_to_action": "Claim Bonus"
        },
        "user_profile": {
            "declared_age": 16,
            "account_verified": False,
            "account_age_days": 200
        },
        "platform_context": "facebook",
        "ground_truth": {
            "correct_decision": "block",
            "acceptable_decisions": ["block"],
            "correct_additional_action": "add_warning_label",
            "minimum_confidence": 0.85,
            "explanation": "Gambling promotions are entirely prohibited for users under 18. Block immediately — no partial restriction applies."
        }
    },

    # ── Scenario 3: Tobacco / Vaping Product ───────────────────────────────
    {
        "case_id": "T1_003",
        "case_type": "content_review",
        "content": {
            "content_type": "advertisement",
            "text": "Discover our new mango-ice vape pods! Smooth hits, incredible flavor. Free shipping on orders over $30. 🌿",
            "image_tags": ["vape", "e-cigarette", "nicotine", "flavored"],
            "advertiser_category": "tobacco_nicotine_product",
            "target_audience_set_by_advertiser": "21+",
            "call_to_action": "Buy Now"
        },
        "user_profile": {
            "declared_age": 14,
            "account_verified": False,
            "account_age_days": 60
        },
        "platform_context": "instagram",
        "ground_truth": {
            "correct_decision": "block",
            "acceptable_decisions": ["block"],
            "correct_additional_action": "add_warning_label",
            "minimum_confidence": 0.85,
            "explanation": "Tobacco and vaping product ads are strictly prohibited from targeting users under 21. Block immediately."
        }
    },

    # ── Scenario 4: Adult Dating App Promotion ─────────────────────────────
    {
        "case_id": "T1_004",
        "case_type": "content_review",
        "content": {
            "content_type": "advertisement",
            "text": "Find your perfect match tonight! Adults-only dating — meet singles near you. Join free. 🔥",
            "image_tags": ["dating", "romance", "adults", "hookup"],
            "advertiser_category": "adult_dating_platform",
            "target_audience_set_by_advertiser": "18+",
            "link_domain": "adultmatch.com",
            "call_to_action": "Join Free"
        },
        "user_profile": {
            "declared_age": 13,
            "account_verified": False,
            "account_age_days": 30
        },
        "platform_context": "instagram",
        "ground_truth": {
            "correct_decision": "block",
            "acceptable_decisions": ["block"],
            "correct_additional_action": "age_gate",
            "minimum_confidence": 0.9,
            "explanation": "Adult dating apps must never be shown to minors. Block immediately and apply age gate."
        }
    },

    # ── Scenario 5: Explicit Violence in Game Ad ───────────────────────────
    {
        "case_id": "T1_005",
        "case_type": "content_review",
        "content": {
            "content_type": "video_advertisement",
            "text": "Brutal. Bloody. Unstoppable. Rated M for Mature. The most violent game of the year is here. Download now.",
            "image_tags": ["violence", "gore", "blood", "mature_rating", "video_game"],
            "advertiser_category": "video_game_mature",
            "esrb_rating": "M (Mature 17+)",
            "video_duration_seconds": 30,
            "call_to_action": "Download Now"
        },
        "user_profile": {
            "declared_age": 13,
            "account_verified": False,
            "account_age_days": 90
        },
        "platform_context": "facebook",
        "ground_truth": {
            "correct_decision": "block",
            "acceptable_decisions": ["block", "restrict"],
            "correct_additional_action": "add_warning_label",
            "minimum_confidence": 0.8,
            "explanation": "Mature-rated game content with explicit violence must be blocked from users under 17."
        }
    },

    # ── Scenario 6: Adult Movie Trailer ────────────────────────────────────
    {
        "case_id": "T1_006",
        "case_type": "content_review",
        "content": {
            "content_type": "promoted_video",
            "text": "Now streaming exclusively on AdultFlix — unrated director's cut. For viewers 18 and above only.",
            "image_tags": ["adult_content", "18+", "unrated", "streaming"],
            "advertiser_category": "adult_entertainment_streaming",
            "content_rating": "Unrated / Adults Only",
            "platform_link": "adultflix.com",
            "call_to_action": "Watch Now"
        },
        "user_profile": {
            "declared_age": 16,
            "account_verified": False,
            "account_age_days": 180
        },
        "platform_context": "threads",
        "ground_truth": {
            "correct_decision": "block",
            "acceptable_decisions": ["block"],
            "correct_additional_action": "age_gate",
            "minimum_confidence": 0.9,
            "explanation": "Adult entertainment content is explicitly prohibited from being shown to users under 18."
        }
    },

    # ── Scenario 7: Online Casino ───────────────────────────────────────────
    {
        "case_id": "T1_007",
        "case_type": "content_review",
        "content": {
            "content_type": "sponsored_post",
            "text": "Play live blackjack, poker and slots from your phone 🃏 New players get 100 free spins! Must be 18+ to play.",
            "image_tags": ["blackjack", "poker", "slots", "casino", "gambling"],
            "advertiser_category": "online_casino",
            "link_domain": "royalbet.io",
            "call_to_action": "Claim Free Spins"
        },
        "user_profile": {
            "declared_age": 17,
            "account_verified": False,
            "account_age_days": 300
        },
        "platform_context": "instagram",
        "ground_truth": {
            "correct_decision": "block",
            "acceptable_decisions": ["block"],
            "correct_additional_action": "add_warning_label",
            "minimum_confidence": 0.85,
            "explanation": "Online casino and gambling content must be blocked for all users under 18, including 17-year-olds."
        }
    },

    # ── Scenario 8: Weapons / Firearms Sale ────────────────────────────────
    {
        "case_id": "T1_008",
        "case_type": "content_review",
        "content": {
            "content_type": "advertisement",
            "text": "Summer sale on handguns, rifles and ammo. Shop our full catalog. Licensed dealer. Free background check included.",
            "image_tags": ["firearm", "gun", "rifle", "handgun", "ammunition", "weapons"],
            "advertiser_category": "firearms_dealer",
            "link_domain": "gunshop-direct.com",
            "call_to_action": "Shop Firearms"
        },
        "user_profile": {
            "declared_age": 15,
            "account_verified": False,
            "account_age_days": 150
        },
        "platform_context": "facebook",
        "ground_truth": {
            "correct_decision": "block",
            "acceptable_decisions": ["block"],
            "correct_additional_action": "add_warning_label",
            "minimum_confidence": 0.85,
            "explanation": "Firearms and weapons sales advertisements must never be shown to users under 18."
        }
    },

    # ── Scenario 9: Adult Entertainment Subscription ───────────────────────
    {
        "case_id": "T1_009",
        "case_type": "content_review",
        "content": {
            "content_type": "sponsored_story",
            "text": "Unlock exclusive adult content from top creators. Subscribe for $9.99/month. 18+ verified platform. 🔞",
            "image_tags": ["adult_content", "subscription", "exclusive", "18+"],
            "advertiser_category": "adult_content_platform",
            "link_domain": "fanonly-adults.com",
            "content_rating": "Adults Only 18+",
            "call_to_action": "Subscribe Now"
        },
        "user_profile": {
            "declared_age": 14,
            "account_verified": False,
            "account_age_days": 45
        },
        "platform_context": "instagram",
        "ground_truth": {
            "correct_decision": "block",
            "acceptable_decisions": ["block"],
            "correct_additional_action": "age_gate",
            "minimum_confidence": 0.95,
            "explanation": "Adult content subscription platforms must be blocked entirely from any user under 18. Highest priority block."
        }
    },

    # ── Scenario 10: Extreme Sports with No Safety Warnings ────────────────
    {
        "case_id": "T1_010",
        "case_type": "content_review",
        "content": {
            "content_type": "advertisement",
            "text": "No helmet. No rules. No limits. 🏍️ Try our extreme stunt bike course — zero safety training required. Book your slot today.",
            "image_tags": ["extreme_sport", "stunt", "motorcycle", "dangerous", "no_safety"],
            "advertiser_category": "extreme_sports_no_safety",
            "safety_warnings_present": False,
            "age_restriction_declared": False,
            "call_to_action": "Book Now"
        },
        "user_profile": {
            "declared_age": 13,
            "account_verified": False,
            "account_age_days": 20
        },
        "platform_context": "threads",
        "ground_truth": {
            "correct_decision": "block",
            "acceptable_decisions": ["block", "restrict"],
            "correct_additional_action": "add_warning_label",
            "minimum_confidence": 0.8,
            "explanation": "Extreme sports content with no safety warnings shown to a 13-year-old must be blocked or restricted with a warning label."
        }
    }

]


def grade_task1(action: dict, ground_truth: dict) -> float:
    """
    Grade an agent's action on Task 1 (Easy) scenarios.

    Scoring (deterministic, always same output for same input):
        +0.70  → Correct decision (exact match)
        +0.40  → Acceptable alternative decision (partial credit)
        +0.15  → Confidence meets or exceeds minimum threshold
        +0.15  → Reason provided and sufficiently detailed (>20 chars)
        Cap at 1.0

    Args:
        action (dict): Agent's action with keys: decision, confidence, reason, additional_action
        ground_truth (dict): Correct answer reference from scenario

    Returns:
        float: Score between 0.0 and 1.0 (rounded to 2 decimal places)
    """
    score = 0.0

    # Decision score.
    agent_decision = str(action.get("decision", "")).strip().lower()
    correct_decision = str(ground_truth.get("correct_decision", "")).strip().lower()
    acceptable_decisions = [d.lower() for d in ground_truth.get("acceptable_decisions", [])]

    if agent_decision == correct_decision:
        score += 0.70
    elif agent_decision in acceptable_decisions:
        score += 0.40

    # Confidence score.
    try:
        agent_confidence = float(action.get("confidence", 0.0))
    except (TypeError, ValueError):
        agent_confidence = 0.0

    minimum_confidence = float(ground_truth.get("minimum_confidence", 0.8))
    if agent_confidence >= minimum_confidence:
        score += 0.15

    # Reason quality score.
    agent_reason = str(action.get("reason", "")).strip()
    if agent_reason and len(agent_reason) > 20:
        score += 0.15

    return round(min(score, 1.0), 2)
