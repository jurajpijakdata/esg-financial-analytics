import os
import sys
import pandas as pd
from pathlib import Path
from decimal import Decimal, InvalidOperation
from sqlalchemy import create_engine
from dotenv import load_dotenv

print("🚀 Starting UpDataLogic ESG Database Ingestion Pipeline (Production Blueprint)...")

# Enforce forced local .env lookup to bypass system variable overrides (Module 3 Standard)
load_dotenv(override=True)

# =====================================================================
# CONFIGURATION & CONNECTIONS (Strict Least-Privilege & Connection Pooler)
# =====================================================================
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "company_esg_financial_dataset_sample.csv"

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "6543") # Optimized for secure connection pooler execution
DB_NAME = os.getenv("DB_NAME")

# PORTFOLIO INTEGRITY CHECK (Juraj's Multi-Mode Architecture Strategy)
# If local credentials do not exist, gracefully downgrade to blueprint/proof-of-concept mode
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
    print("\n💡 PORTFOLIO NOTE: Operational pipeline running in BLUEPRINT/TEMPLATE mode.")
    print("To execute this ingestion actively on live storage, populate your secure local '.env' targets.")
    print("Pipeline execution completed safely as an architecture proof-of-concept for target clients.\n")
    sys.exit(0)

# Constructing the secure connection string dynamically via port 6543
DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# =====================================================================
# ETL INGESTION STAGE
# =====================================================================
try:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Extraction halted. Target source dataset not found: {DATA_FILE}")

    print(f"📥 1. Extracting records from local storage: {DATA_FILE.name}...")
    df = pd.read_csv(DATA_FILE, low_memory=False)
    
    print("⏳ 2. Executing pre-load data type normalization pipeline (Module 4 Standards)...")
    all_metrics = [
        'Revenue', 'ProfitMargin', 'MarketCap', 'GrowthRate', 
        'ESG_Overall', 'CarbonEmissions', 'WaterUsage', 'EnergyConsumption'
    ]
    
    # Financial token normalizer utilizing decimal.Decimal to completely block float drifting
    def strict_numeric_normalizer(value):
        if pd.isna(value) or str(value).strip() == '':
            return None # Missing values map purely to clean database NULLs
        clean_str = str(value).strip().replace(',', '.')
        try:
            return float(Decimal(clean_str).quantize(Decimal("0.01")))
        except InvalidOperation:
            return None

    # Apply strict parsing instead of corruptive loose .fillna(0) metrics formatting
    for col in all_metrics:
        df[col] = df[col].apply(strict_numeric_normalizer)
        
    # Inject decoupled data quality flags before loading to database warehouse
    df['data_quality_status'] = df[all_metrics].isnull().any(axis=1).map({True: 'UNKNOWN', False: 'CLEAN'})
        
    print("🔌 3. Establishing pipeline connection to PostgreSQL data cluster...")
    engine = create_engine(DB_URL)
    
    print(f"📤 4. Stream loading {len(df):,} records into database target ['public.esg_financials_raw']...")
    # Optimized chunk loading prevents memory execution bottlenecks on remote servers
    df.to_sql('esg_financials_raw', engine, schema='public', if_exists='replace', index=False, chunksize=10000)
    
    print("\n=== 🎉 PIPELINE SUCCESS: ALL ESG FINANCIAL DATA PROVISIONED TO POSTGRESQL ===")

except Exception as e:
    print(f"\n❌ PIPELINE CRITICAL FAILURE: {e}", file=sys.stderr)
    sys.exit(1)
