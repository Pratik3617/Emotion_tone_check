from typing import Optional


REWRITE_RULES = {
    ("negative", "low"): "Just checking in on this.",
    ("negative", "medium"): "Could you please share an update on this?",
    ("negative", "high"): "I might be mistaken, but could we review this together?",

    ("neutral", "low"): None,  # No rewrite needed
    ("neutral", "medium"): "Just checking in on this.",
    ("neutral", "high"): "Could you please share an update on this?",

    ("positive", "low"): None,  # No rewrite needed
    ("positive", "medium"): "Thanks for the update!",
    ("positive", "high"): "Thanks for the update!",
}


def suggest_rewrite(tone: str, risk_level: str) -> Optional[str]:
    """
    Suggest a safer rewrite based on tone and risk.
    Returns None if no rewrite is required.
    """
    return REWRITE_RULES.get((tone, risk_level))
