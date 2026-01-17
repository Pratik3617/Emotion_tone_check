import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from pathlib import Path

# saved model checkpoint path
MODEL_DIR = Path("../models/emotion_model/checkpoint-2714")

_MODEL = None
_TOKENIZER = None
_DEVICE = None


# Helper functions
def _select_device():
    """Select compute device."""
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


# Public API
def load_model_and_tokenizer():
    """
    Load model and tokenizer once (singleton).
    safe to call multiple times
    """
    global _MODEL, _TOKENIZER, _DEVICE

    if _MODEL is not None and _TOKENIZER is not None and _DEVICE is not None:
        return _MODEL, _TOKENIZER, _DEVICE

    if not MODEL_DIR.exists():
        raise FileNotFoundError(
            f"Model directory not found at: {MODEL_DIR.resolve()}"
        )

    _DEVICE = _select_device()

    _TOKENIZER = AutoTokenizer.from_pretrained(MODEL_DIR)

    _MODEL = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
    _MODEL.to(_DEVICE)
    _MODEL.eval()

    return _MODEL, _TOKENIZER, _DEVICE


def get_model():
    model, _, _ = load_model_and_tokenizer()
    return model


def get_tokenizer():
    _, tokenizer, _ = load_model_and_tokenizer()
    return tokenizer


def get_device():
    _, _, device = load_model_and_tokenizer()
    return device