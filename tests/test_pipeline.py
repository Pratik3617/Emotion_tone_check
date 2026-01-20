import pytest

from inference.pipeline import analyze_tone


@pytest.mark.parametrize(
    "text, expected_risk",
    [
        ("Thanks a lot for helping me with this!", "low"),
        ("This should have been done already.", "low"),
        ("I don’t think this approach makes sense.", "medium"),
        ("Please fix this immediately, this is unacceptable.", "high"),
    ],
)

def test_pipeline_risk_levels(text, expected_risk):
    """
    Verify that the pipeline assigns correct risk levels
    for representative inputs.
    """
    result = analyze_tone(text)

    assert "risk_level" in result
    assert result["risk_level"] == expected_risk


def test_pipeline_structure():
    """
    Verify that pipeline output contains all expected fields.
    """
    text = "Please review this when you get a chance."
    result = analyze_tone(text)

    expected_keys = {
        "input_text",
        "tone",
        "tone_scores",
        "risk_score",
        "risk_level",
        "suggested_rewrite",
        "flags",
        "requires_attention",
    }

    assert expected_keys.issubset(result.keys())


def test_pipeline_rewrite_behavior():
    """
    Verify rewrite behavior matches risk severity.
    """
    low_risk = analyze_tone("Thanks for your help!")
    assert low_risk["suggested_rewrite"] is None

    medium_risk = analyze_tone("I don’t think this approach makes sense.")
    assert medium_risk["suggested_rewrite"] is not None

    high_risk = analyze_tone("Please fix this immediately.")
    assert high_risk["suggested_rewrite"] is not None


def test_pipeline_requires_attention_flag():
    """
    Verify requires_attention flag logic.
    """
    low = analyze_tone("Thanks for the update!")
    assert low["requires_attention"] is False

    medium = analyze_tone("I don’t think this approach makes sense.")
    assert medium["requires_attention"] is True

    high = analyze_tone("Fix this immediately.")
    assert high["requires_attention"] is True
