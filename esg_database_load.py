import sys
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

print("🚀 Starting UpDataLogic ESG Database Ingestion Pipeline...")

# =====================================================================
# CONFIGURATION & CONNECTIONS
# =====================================================================
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "company_esg_financial_dataset.csv"

# Production Connection String (To be migrated to secure .env environment variables later)
DB_URL = 'postgresql+psycopg2://YOUR_DATABASE_USER:YOUR_DATABASE_PASSWORD@YOUR_DATABASE_HOST:5432/YOUR_DATABASE_NAME'

# =====================================================================
# ETL INGESTION STAGE
# =====================================================================
try:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Extraction halted. Target source dataset not found: {DATA_FILE}")

    print(f"📥 1. Extracting records from local storage: {DATA_FILE.name}...")
    df = pd.read_csv(DATA_FILE, low_memory=False)
    
    print("⏳ 2. Executing pre-load data type normalization pipeline...")
    all_numeric = [
        'Revenue', 'ProfitMargin', 'MarketCap', 'GrowthRate', 
        'ESG_Overall', 'CarbonEmissions', 'WaterUsage', 'EnergyConsumption'
    ]
    for col in all_numeric:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
    print("🔌 3. Establishing pipeline connection to PostgreSQL data cluster...")
    engine = create_engine(DB_URL)
    
    print(f"📤 4. Stream loading {len(df):,} records into database target ['public.esg_financials_raw']...")
    # Optimized chunk loading prevents memory execution bottlenecks on remote servers
    df.to_sql('esg_financials_raw', engine, schema='public', if_exists='replace', index=False, chunksize=10000)
    
    print("\n=== 🎉 PIPELINE SUCCESS: ALL ESG FINANCIAL DATA PROVISIONED TO POSTGRESQL ===")

except Exception as e:
    # HARD FAILURE SIGNALING (UpDataLogic Rule 3)
    print(f"\n❌ PIPELINE CRITICAL FAILURE: {e}", file=sys.stderr)
    sys.exit(1)
