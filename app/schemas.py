from pydantic import BaseModel, Field, field_validator
from typing import Dict, Optional, List

class AnalyzeToneRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=500, description="Input message text")
    @field_validator("text")
    def text_must_have_words(cls, v):
        if len(v.split()) < 2:
            raise ValueError("Text must contain at least two words")
        return v

class AnalyzeToneResponse(BaseModel):
    input_text: str
    tone: str
    tone_scores: Optional[Dict[str, float]] = None
    risk_score: float
    risk_level: str
    suggested_rewrite: Optional[str]

    flags: List[str]
    requires_attention: bool