import sys
import pandas as pd
from pathlib import Path

print("🚀 Starting UpDataLogic ESG & Financial Analytics Engine...")

# =====================================================================
# DYNAMIC PATH RESOLUTION (UpDataLogic Rule 2)
# =====================================================================
# Automatically detect the directory where this script is located
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "company_esg_financial_dataset.csv"

# =====================================================================
# DATA PIPELINE EXECUTION
# =====================================================================
try:
    # Fail fast if the dataset is missing from the working directory
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Critical data resource missing at targeted path: {DATA_FILE}")
        
    print(f"📥 Loading raw dataset: {DATA_FILE.name}...")
    df = pd.read_csv(DATA_FILE, low_memory=False)
    
    print("\n🔍 Auditing dataset for missing values (NaN)...")
    missing_data = df[['Revenue', 'ProfitMargin', 'MarketCap', 'ESG_Overall']].isnull().sum()
    print(missing_data)
    
    print("\n⏳ Executing strict financial and ESG data cleansing pipeline...")
    # Sanitize core financial KPIs
    financial_columns = ['Revenue', 'ProfitMargin', 'MarketCap', 'GrowthRate', 'ESG_Overall']
    for column in financial_columns:
        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)
        
    # Sanitize environmental footprint metrics
    env_columns = ['CarbonEmissions', 'WaterUsage', 'EnergyConsumption']
    for column in env_columns:
        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)
        
    print("\n=== 🎉 DATA CLEANSING COMPLETED SUCCESSFULLY ===")
    print(f"Processed Rows: {df.shape[0]:,}")
    print(f"Processed Columns: {df.shape[1]}")
    
    # Core business insight generation
    print("\n=== 📊 QUICK INSIGHT: AVG PROFIT MARGIN BY INDUSTRY ===")
    avg_margin = df.groupby('Industry')['ProfitMargin'].mean().sort_values(ascending=False)
    print(avg_margin)
    print("\n🏆 ANALYTICS RUN COMPLETED SUCCESSFULLY.")

except Exception as e:
    # HARD FAILURE SIGNALING (UpDataLogic Rule 3)
    print(f"\n❌ PIPELINE CRITICAL FAILURE: {e}", file=sys.stderr)
    sys.exit(1)
