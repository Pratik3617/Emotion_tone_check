from fastapi import FastAPI, HTTPException, Query
from app.schemas import AnalyzeToneRequest, AnalyzeToneResponse
from inference.pipeline import analyze_tone
from pydantic import ValidationError
import time
from app_logging.logger import setup_logger

logger = setup_logger()

app = FastAPI(
    title="Emotion Aware TOne & Risk Analyzer",
    version="1.0.0"
)

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
    response_model_exclude_none=True,
    summary="Analyze emotional tone and communication risk",
    description="Detects tone, evaluates risk, and suggests safer rewrites"
)

def analyze_tone_endpoint(
    request: AnalyzeToneRequest, 
    include_scores: bool = Query(True, description="Include tone score breakdown")
):
    start_time = time.time()

    try:
        logger.info("Received analyze-tone request")

        result = analyze_tone(request.text)
        if not include_scores:
            result.pop("tone_scores", None)
        
        logger.info(
            "Analysis completed | tone=%s | risk=%s | rewrite=%s",
            result["tone"],
            result["risk_level"],
            result["suggested_rewrite"] is not None,
        )

        return result
    except ValidationError as e:
        logger.warning("Validation error: %s", e)
        raise HTTPException(status_code=422, detail=e.errors())
    except ValueError as e:
        logger.warning("Bad request: %s", e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("Unexpected error during analysis")
        raise HTTPException(status_code=500, detail="Internal error during tone analysis")
    
    finally:
        duration = round(time.time() - start_time, 3)
        logger.info("Request processed in %ss", duration)