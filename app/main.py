from fastapi import FastAPI, HTTPException, Query
from app.schemas import AnalyzeToneRequest, AnalyzeToneResponse
from inference.pipeline import analyze_tone
from pydantic import ValidationError

app = FastAPI(
    title="Emotion-Aware Tone & Risk Analyzer",
    description="Analyze emotional tone, communication risk, and suggest safer rewrite",
    version="1.0.0"
)

@app.get('/health')
def health_check():
    return {"status":"ok"}

@app.post("/analyze-tone", 
    response_model=AnalyzeToneResponse, 
    summary="Analyze emotional tone and communication risk",
    description="Detects tone, evaluates risk, and suggests safer rewrites"
)

def analyze_tone_endpoint(
    request: AnalyzeToneRequest, 
    include_scores: bool = Query(True, description="Include tone score breakdown")
):
    try:
        result = analyze_tone(request.text)
        if not include_scores:
            result.pop("tone_scores")
        return result
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal error during tone analysis")