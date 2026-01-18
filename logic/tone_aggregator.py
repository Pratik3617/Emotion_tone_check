from typing import Dict, Tuple

NEGATIVE_EMOTIONS = [
    "anger",
    "annoyance",
    "disapproval",
    "disappointment",
    "disgust",
    "sadness",
    "remorse",
]

POSITIVE_EMOTIONS = [
    "gratitude",
    "joy",
    "love",
    "optimism",
    "approval",
    "admiration",
    "relief",
    "pride",
]

NEUTRAL_EMOTIONS = [
    "neutral",
    "realization",
    "confusion",
    "curiosity",
    "surprise",
]

def aggregate_tone(emotion_scores: Dict[str, float]) -> Tuple[str, Dict[str, float]]:
    """
    Aggregate fine-grained emotions into coarse tone
    """

    negative = sum(emotion_scores.get(e, 0.0) for e in NEGATIVE_EMOTIONS)
    positive = sum(emotion_scores.get(e, 0.0) for e in POSITIVE_EMOTIONS)
    neutral = sum(emotion_scores.get(e, 0.0) for e in NEUTRAL_EMOTIONS)

    tone_scores = {
        "negative": negative,
        "positive": positive,
        "neutral": neutral
    }

    tone = max(tone_scores, key=tone_scores.get)

    return tone, tone_scores