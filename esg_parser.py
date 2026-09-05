import pandas as pd
from decimal import Decimal, InvalidOperation
from typing import Any, Optional

def clean_esg_numeric_vector(value: Any) -> Optional[Decimal]:
    """
    Safely normalizes and validates corporate financial inputs without silent zero corruption.

    This function strips potential spacing anomalies and standardizes European/US comma system 
    separators into clean numeric tokens. Malformed, incomplete, or corrupted items are mapped 
    directly to strict None to register transparently inside downstream quarantine quality trackers.

    Args:
        value (Any): The raw corporate financial column slice (e.g., Revenue, ProfitMargin).

    Returns:
        Optional[Decimal]: A sanitized high-precision Decimal object for accounting calculations, 
                           or None if unparseable tokens or drift anomalies are isolated.
    """
    if pd.isna(value) or str(value).strip() == '':
        return None
    
    clean_str: str = str(value).strip().replace(',', '.')
    try:
        return Decimal(clean_str)
    except InvalidOperation:
        return None

def classify_esg_investment_tier(score: Any) -> str:
    """
    Classifies global corporate assets into deterministic tiers based on active sustainability scores.

    Args:
        score (Any): The validated numerical ESG overall score attribute.

    Returns:
        str: A standardized enterprise investment tier string classification tag, 
             or 'UNKNOWN' if structural data noise is captured.
    """
    if score is None or pd.isna(score):
        return 'UNKNOWN'
    try:
        numeric_score: float = float(score)
        if numeric_score >= 75:
            return 'ESG Leader (High Sustainability)'
        elif numeric_score >= 40:
            return 'ESG Average (Medium Sustainability)'
        else:
            return 'ESG Laggard (Low Sustainability)'
    except (ValueError, TypeError):
        return 'UNKNOWN'
