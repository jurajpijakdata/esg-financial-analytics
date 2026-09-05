import pandas as pd
from decimal import Decimal, InvalidOperation

def clean_esg_numeric_vector(value):
    """
    Safely normalizes and validates corporate financial inputs without silent zero corruption.
    Returns Decimal objects for precision or None for malformed tokens to isolate inside quarantine trackers.
    """
    if pd.isna(value) or str(value).strip() == '':
        return None
    
    clean_str = str(value).strip().replace(',', '.')
    try:
        return Decimal(clean_str)
    except InvalidOperation:
        return None

def classify_esg_investment_tier(score):
    """
    Classifies global assets based on deterministic sustainability scores.
    """
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
