from typing import Dict, Optional
from inference.predictor import predict_emotions
from logic.tone_aggregator import aggregate_tone
from logic.risk_scorer import compute_risk_score, risk_level, override_risk_level_for_soft_disagreement
from logic.rewrite_engine import suggest_rewrite

def analyze_tone(text: str) -> Dict[str, Optional[object]]:
    """
    Analyze the tone and risk

    Args: 
        text(str) : Input message text

    Returns:
        dict: Analysis result containing tone, risk, and rewrite
    """
    if not text or not isinstance(text, str):
        raise ValueError("Input text must be a non-empty string")
    
    # compute emotion scores
    emotion_scores = predict_emotions(text)

    # compute tone of the text
    tone, tone_scores = aggregate_tone(emotion_scores)

    # risk analysis
    risk_score = compute_risk_score(emotion_scores, text)

    intial_risk_level = risk_level(risk_score)

    # buisness rule override 
    final_risk_level = override_risk_level_for_soft_disagreement(intial_risk_level, text)

    # assign flags
    flags = []
    if final_risk_level == "high":
        flags.append("urgent_review")
    if final_risk_level in ("medium", "high"):
        flags.append("tone_sensitive")

    requires_attention = final_risk_level != "low"


    # rewrite suggestions
    rewrite = suggest_rewrite(tone, final_risk_level)

    return{
        "input_text": text,
        "tone": tone,
        "tone_scores": {
            k : float(v) for k, v in tone_scores.items()
        },
        "risk_score": round(float(risk_score), 3),
        "risk_level": final_risk_level,
        "suggested_rewrite": rewrite,
        "flags": flags,
        "requires_attention": requires_attention
    }
