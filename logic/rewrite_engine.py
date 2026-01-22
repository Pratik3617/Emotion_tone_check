from typing import Optional
from llm.rewrite_generator import generate_rewrite

TEMPLATE_REWRITES = {
    ("negative", "medium"): "Could you please share an update on this?",
    ("negative", "high"): "I might be mistaken, but could we review this together?",
}


def suggest_rewrite(text: str, tone: str, risk_level: str) -> Optional[str]:
    """
    Hybrid rewrite engine:
    - Low risk → no rewrite
    - Medium risk → LLM (fallback to template)
    - High risk → LLM (fallback to template)
    """

    if risk_level == "low":
        return None

    # LLM for medium & high risk
    if risk_level in ("medium", "high"):
        try:
            rewrite = generate_rewrite(text)

            # Safety check: empty or nonsense output
            if not rewrite or len(rewrite.strip()) < 5:
                raise ValueError("Invalid LLM rewrite")

            return rewrite

        except Exception:
            # Safe deterministic fallback
            return TEMPLATE_REWRITES.get(
                (tone, risk_level),
                TEMPLATE_REWRITES.get(
                    (tone, "medium"),
                    "Could you please share an update on this?",
                ),
            )

    return None
