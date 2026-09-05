import os
import sys
import logging
import pandas as pd
import pandera.pandas as pa
from pathlib import Path
from sqlalchemy import create_engine
from dotenv import load_dotenv

# =====================================================================
# ENTERPRISE LOGGING CONFIGURATION (Module 6 Standard)
# =====================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [UpDataLogic Ingestion] - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logging.info("🚀 Starting UpDataLogic ESG Database Ingestion Pipeline (Production Observability Mode)...")

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "company_esg_financial_dataset_sample.csv"
ENV_FILE = BASE_DIR / ".env"

# 1. Define Strict Data Quality Ingestion Shield via Pandera
esg_ingest_schema = pa.DataFrameSchema({
    "CompanyID": pa.Column(str, nullable=False),
    "CompanyName": pa.Column(str, nullable=False),
    "Industry": pa.Column(str, nullable=False),
    "Region": pa.Column(str, nullable=False)
})

# 2. Database Connection Check with Dynamic Fallback Context Routing
try:
    if ENV_FILE.exists():
        load_dotenv(dotenv_path=ENV_FILE, override=True)
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT", "6543")
        DB_NAME = os.getenv("DB_NAME")
        
        if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
            raise ValueError("Incomplete database parameters inside .env.")
            
        connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(connection_string)
        with engine.connect() as conn:
            pass
        logging.info("🔌 Connection Status: [ONLINE] Remote PostgreSQL Warehouse Connected.")
    else:
        raise FileNotFoundError("Local configuration env targets missing.")

except Exception as db_error:
    logging.warning(f"⚠️ Production DB Offline or Network Issue detected: {db_error}")
    logging.info("🔄 Activating Portfolio Architecture Fallback Mode (Local Standalone Engine)...")
    connection_string = f"sqlite:///{BASE_DIR / 'local_portfolio.db'}"
    engine = create_engine(connection_string)
    logging.info("🔌 Connection Status: [LOCAL ENGINE] Active Fallback SQLite Context Deployed.")

# =====================================================================
# ETL INGESTION STAGE Execution Layers
# =====================================================================
try:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Extraction halted. Source dataset missing at: {DATA_FILE}")

    logging.info(f"📥 1. EXTRACTION: Reading raw records from target file: {DATA_FILE.name}")
    df = pd.read_csv(DATA_FILE, dtype={"CompanyID": str}, low_memory=False)
    
    logging.info("⏳ 2. TRANSFORMATION: Executing structural data pre-load alignment matrices...")
    
    # Clean financial metrics formatting proactively before validation layer execution
    for col in ['Revenue', 'ProfitMargin', 'MarketCap', 'GrowthRate']:
        df[col] = df[col].astype(str).str.replace(',', '', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')

    logging.info("🛡️ 3. VALIDATION: Running structural data quality tests via Pandera schema evaluation...")
    validated_df = esg_ingest_schema.validate(df)
    
    logging.info(f"📤 4. LOADING: Streaming {len(validated_df):,} validated records into target warehouse registries...")
    validated_df.to_sql('esg_financials_raw', engine, if_exists='replace', index=False)
    
    logging.info("🏆 PIPELINE RUN COMPLETION: STATUS 0 [SUCCESS]. All data streamed to database layer.\n")
    sys.exit(0) # Enforce strict safe process telemetry states for orchestrators

except pa.errors.SchemaError as schema_fault:
    logging.critical(f"❌ PIPELINE STOPPED VIA PANDERA INGESTION SHIELD: {schema_fault}")
    sys.exit(1) # Enforce failure code to alert cloud scheduling triggers
except Exception as fatal_error:
    logging.critical(f"❌ PIPELINE INGESTION CRITICAL RUNTIME FAILURE: {fatal_error}")
    sys.exit(1)
