import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_health_check():
    """
    verify health endpoints works.
    """
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}

def test_analyze_tone_no_rewrite_for_low_risk():
    payload = {
        "text": "Thanks for helping me with this!"
    }

    response = client.post("/analyze-tone", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["risk_level"] == "low"
    assert "suggested_rewrite" not in data


def test_analyze_tone_rewrite_present_for_risky_input():
    payload = {
        "text": "Please fix this immediately, this is unacceptable."
    }

    response = client.post("/analyze-tone", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["risk_level"] in ("medium", "high")
    assert "suggested_rewrite" in data
    assert isinstance(data["suggested_rewrite"], str)



def test_analyze_tone_include_scores_false():
    """
    verify include_scores=false does not break API
    """
    payload = {
        "text": "I don’t think this approach makes sense."
    }

    response = client.post("/analyze-tone?include_scores=false", json=payload)

    assert response.status_code==200
    data = response.json()
    assert "tone_scores" not in data

def test_analyze_tone_validation_error():
    """
    Verify validation error for short / invalid input.
    """
    payload = {
        "text": "ok"
    }
    response = client.post('/analyze-tone', json=payload)

    assert response.status_code == 422

def test_analyze_tone_missing_text():
    """
    Verify validation error when text is missing.
    """
    response = client.post('analyze-tone',json={})

    assert response.status_code == 422
