import os
import sys
import pandas as pd
from pathlib import Path
from decimal import Decimal, InvalidOperation

print("🚀 Starting UpDataLogic ESG & Financial Analytics Engine (Enhanced Integrity)...")

# =====================================================================
# DYNAMIC PATH RESOLUTION (UpDataLogic Rule 2)
# =====================================================================
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "company_esg_financial_dataset_sample.csv"

# =====================================================================
# DATA PIPELINE EXECUTION
# =====================================================================
try:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Critical data resource missing at targeted path: {DATA_FILE}")
        
    print(f"📥 Loading raw dataset: {DATA_FILE.name}...")
    df = pd.read_csv(DATA_FILE, low_memory=False)
    
    print("\n🔍 Auditing dataset for missing values (NaN)...")
    financial_columns = ['Revenue', 'ProfitMargin', 'MarketCap', 'GrowthRate', 'ESG_Overall']
    env_columns = ['CarbonEmissions', 'WaterUsage', 'EnergyConsumption']
    print(df[financial_columns + env_columns].isnull().sum())
    
    print("\n⏳ Executing strict financial and ESG data cleansing pipeline...")
    
    # Robust Financial & ESG Decimal Parser matching Module 4 Correctness constraints
    # Prevents .fillna(0) from corrupting downstream arithmetic aggregates like .mean()
    def robust_decimal_parser(value):
        if pd.isna(value) or str(value).strip() == '':
            return None # Keeps missing values as clean NULL instead of masking with artificial zeros
        
        clean_str = str(value).strip().replace(',', '.')
        try:
            # Enforce high-precision Decimal scales to eliminate binary float drifting
            return Decimal(clean_str)
        except InvalidOperation:
            return None

    # Apply strict parsing across all metric vectors
    all_metrics = financial_columns + env_columns
    for column in all_metrics:
        df[column] = df[column].apply(robust_decimal_parser)
        
    # DECOUPLED QUALITY FLAGS: Ensure measure metrics remain numerical for aggregations
    df['data_quality_status'] = df[all_metrics].isnull().any(axis=1).map({True: 'UNKNOWN', False: 'CLEAN'})
    
    print("\n=== 🎉 DATA CLEANSING COMPLETED SUCCESSFULLY ===")
    print(f"Processed Rows: {df.shape[0]:,}")
    print(f"Processed Columns: {df.shape[1]}")
    
    # Core business insight generation (Safe mean calculation ignoring NULLs, preserving accuracy)
    print("\n=== 📊 QUICK INSIGHT: AVG PROFIT MARGIN BY INDUSTRY (VERIFIED) ===")
    # Convert back to float purely for pandas plotting/groupby aggregates representation
    df['ProfitMargin_Float'] = df['ProfitMargin'].astype(float)
    avg_margin = df.groupby('Industry')['ProfitMargin_Float'].mean().sort_values(ascending=False)
    print(avg_margin)
    
    print("\n🏆 ANALYTICS RUN COMPLETED SUCCESSFULLY.")

except Exception as e:
    print(f"\n❌ PIPELINE CRITICAL FAILURE: {e}", file=sys.stderr)
    sys.exit(1)
