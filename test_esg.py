import pytest
import pandas as pd
from decimal import Decimal, InvalidOperation

# =====================================================================
# 1. PURE TRANSFORM FUNCTIONS (Extracted for Validation)
# =====================================================================
def clean_esg_numeric_vector(value):
    """Safely normalizes and validates corporate financial inputs without zero corruption."""
    if pd.isna(value) or str(value).strip() == '':
        return None
    
    clean_str = str(value).strip().replace(',', '.')
    try:
        return Decimal(clean_str)
    except InvalidOperation:
        raise ValueError(f"Data conversion crash for token: {value}")

def classify_esg_investment_tier(score):
    """Classifies global assets based on deterministic sustainability scores."""
    if score is None:
        return 'UNKNOWN'
    try:
        numeric_score = float(score)
        if numeric_score >= 75:
            return 'ESG Leader (High Sustainability)'
        elif numeric_score >= 40:
            return 'ESG Average (Medium Sustainability)'
        else:
            return 'ESG Laggard (Low Sustainability)'
    except (ValueError, TypeError):
        return 'UNKNOWN'


# =====================================================================
# 2. PYTEST SUITE SIMULATION
# =====================================================================

@pytest.mark.parametrize("input_val, expected_output", [
    ("1250000.50", Decimal("1250000.50")),
    ("34.15", Decimal("34.15")),
    ("  89.00  ", Decimal("89.00")),
])
def test_clean_esg_numeric_vector_valid_cases(input_val, expected_output):
    """Verifies floating point casting and spacing extractions."""
    assert clean_esg_numeric_vector(input_val) == expected_output


def test_clean_esg_numeric_vector_catches_text_corruption():
    """Verifies that unparseable alphanumeric strings force an explicit exception."""
    with pytest.raises(ValueError, match="Data conversion crash for token"):
        clean_esg_numeric_vector("CORRUPTED_TEXT")


def test_classify_esg_investment_tier_logic():
    """Verifies business rule classification for corporate investment tiers."""
    assert classify_esg_investment_tier(82) == 'ESG Leader (High Sustainability)'
    assert classify_esg_investment_tier(55) == 'ESG Average (Medium Sustainability)'
    assert classify_esg_investment_tier(20) == 'ESG Laggard (Low Sustainability)'
    assert classify_esg_investment_tier("INVALID") == 'UNKNOWN'
