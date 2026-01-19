from logic.text_normalizer import normalize_text
from typing import Dict

# Emotion → risk contribution
RISK_WEIGHTS = {
    "anger": 0.35,
    "annoyance": 0.30,
    "disapproval": 0.30,
    "disgust": 0.15,
    "sadness": 0.10,
}

URGENT_KEYWORDS = [
    "immediately",
    "asap",
    "urgent",
    "unacceptable",
    "right now",
    "fix this",
    "must be done",
    "do this now",
]

SOFT_DISAGREEMENT_PHRASES = [
    "i don't think",
    "i dont think",
    "i do not think",
    "doesn't make sense",
    "does not make sense",
    "i disagree",
    "i'm not sure this",
]

def urgency_multiplier(text: str) -> float:
    text = normalize_text(text)
    return 1.5 if any(k in text for k in URGENT_KEYWORDS) else 1.0

def disagreement_discount(text: str) -> float:
    text = normalize_text(text)
    return 0.7 if any(k in text for k in SOFT_DISAGREEMENT_PHRASES) else 1.0

def compute_risk_score(emotion_scores: Dict[str, float], text: str) -> float:
    """
    Compute continuous risk score
    """
    base_risk = 0.0
    for emotion, weight in RISK_WEIGHTS.items():
        base_risk += weight * emotion_scores.get(emotion, 0.0) # if any emotion is missing -> contributes 0.0

    risk = base_risk
    risk *= urgency_multiplier(text)
    risk *= disagreement_discount(text)

    return risk

def risk_level(score: float) -> str:
    """
    convert continuous risk to discrete level
    """
    if score >= 0.18:
        return "high"
    if score >= 0.08:
        return "medium"
    return "low"

def override_risk_level_for_soft_disagreement(level: str, text: str) -> str:
    """
    Enforce business rule:
    Constructive disagreement without urgency is never high risk
    """
    text = normalize_text(text)
    has_disagreement = has_disagreement = disagreement_discount(text) < 1.0
    has_urgency = urgency_multiplier(text) > 1.0

    if has_disagreement and not has_urgency:
        return "medium"
    
    return level