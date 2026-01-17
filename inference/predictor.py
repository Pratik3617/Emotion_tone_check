from typing import Dict
import torch
from pathlib import Path
import json
from model_loader import (
    get_model, get_tokenizer, get_device
)

LABELS_PATH = Path("../config/emotion_labels.json")

with open(LABELS_PATH, "r") as f:
    EMOTION_LABELS = json.load(f)


def predict_emotions(text: str) -> Dict[str, float]:
    if not text or not isinstance(text, str):
        raise ValueError("Input text must be a non-empty string")
    
    model = get_model()
    tokenizer = get_tokenizer()
    device = get_device()

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=128
    )

    # map input and model to same device
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # turn off gradient tracking for inference, evaluation and memory efficiency
    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.sigmoid(outputs.logits)[0].cpu().numpy()


    emotion_scores = {
        EMOTION_LABELS[i]: float(probs[i]) for i in range(len(EMOTION_LABELS))
    }

    return emotion_scores