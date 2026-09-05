import pytest
from decimal import Decimal
# Import the actual pure production code functions to prevent lab ghost duplicates
from esg_parser import clean_esg_numeric_vector, classify_esg_investment_tier

@pytest.mark.parametrize("input_val, expected_output", [
    ("1250000.50", Decimal("1250000.50")),
    ("34.15", Decimal("34.15")),
    ("  89.00  ", Decimal("89.00")),
    ("", None),
])
def test_clean_esg_numeric_vector_valid_cases(input_val, expected_output):
    """Verifies floating point casting and spacing extractions across corporate financial layers."""
    assert clean_esg_numeric_vector(input_val) == expected_output


def test_clean_esg_numeric_vector_catches_text_corruption():
    """Verifies that unparseable text payloads inside financial vectors return None for tracking metrics."""
    assert clean_esg_numeric_vector("CORRUPTED_TEXT") is None


def test_classify_esg_investment_tier_logic():
    """Verifies rule-based sustainability segment classification mappings."""
    assert classify_esg_investment_tier(82) == 'ESG Leader (High Sustainability)'
    assert classify_esg_investment_tier(55) == 'ESG Average (Medium Sustainability)'
    assert classify_esg_investment_tier(20) == 'ESG Laggard (Low Sustainability)'
    assert classify_esg_investment_tier("INVALID") == 'UNKNOWN'
