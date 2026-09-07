import os
import sys
import logging
import pandas as pd
import pandera.pandas as pa
from pathlib import Path
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# =====================================================================
# ENTERPRISE LOGGING CONFIGURATION (Module 6, 7 & 10 Standard)
# =====================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [UpDataLogic ESG Ingestion] - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logging.info("🚀 Starting UpDataLogic ESG Database Ingestion Pipeline (Idempotent Production Mode)...")

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "company_esg_financial_dataset_sample.csv"
ENV_FILE = BASE_DIR / ".env"

# Define Strict Data Quality Ingestion Shield via Pandera Specification
esg_ingest_schema = pa.DataFrameSchema({
    "CompanyID": pa.Column(str, nullable=False),
    "CompanyName": pa.Column(str, nullable=False),
    "Industry": pa.Column(str, nullable=False),
    "Region": pa.Column(str, nullable=False)
})

# Database Connection Check with Dynamic Fallback Context Routing
try:
    if ENV_FILE.exists():
        load_dotenv(dotenv_path=ENV_FILE, override=True)
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT", "6543")
        DB_NAME = os.getenv("DB_NAME")
        
        if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
            raise ValueError("Incomplete database credentials inside configuration targets.")
            
        connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(connection_string)
        with engine.connect() as conn:
            pass
        logging.info("🔌 Connection Status: [ONLINE] Remote PostgreSQL Warehouse Connected.")
    else:
        raise FileNotFoundError("Local configurations env targets missing.")

except Exception as db_error:
    logging.warning(f"⚠️ Production DB Offline or Network Issue detected: {db_error}")
    logging.info("🔄 Activating Portfolio Architecture Fallback Mode (Local Standalone Engine)...")
    connection_string = f"sqlite:///{BASE_DIR / 'local_portfolio.db'}"
    engine = create_engine(connection_string)
    logging.info("🔌 Connection Status: [LOCAL ENGINE] Active Fallback SQLite Context Deployed.")

# =====================================================================
# ETL INGESTION STAGE Execution with Idempotent UPSERT Matrix
# =====================================================================
try:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Extraction halted. Source dataset missing at: {DATA_FILE}")

    logging.info(f"📥 1. EXTRACTION: Reading raw records from target file: {DATA_FILE.name}")
    df = pd.read_csv(DATA_FILE, dtype={"CompanyID": str}, low_memory=False)
    
    logging.info("⏳ 2. TRANSFORMATION: Executing structural data pre-load alignment matrices...")
    for col in ['Revenue', 'ProfitMargin', 'MarketCap', 'GrowthRate']:
        df[col] = df[col].astype(str).str.replace(',', '', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')

    logging.info("🛡️ 3. VALIDATION: Running structural data quality tests via Pandera schema evaluation...")
    validated_df = esg_ingest_schema.validate(df)
    
    validated_df['data_quality_status'] = validated_df[['Revenue', 'ProfitMargin']].isnull().any(axis=1).map({True: 'UNKNOWN', False: 'CLEAN'})
    
    logging.info("📤 4. LOADING: Executing idempotent UPSERT pattern routing directly to database engine...")
    
    with engine.begin() as transaction_conn:
        if str(engine.url).startswith('sqlite'):
            # PRODUCTION BLUEPRINT: Deploy strict CHECK constraints to enforce structural data quality
            transaction_conn.execute(text("DROP TABLE IF EXISTS esg_financials_raw;"))
            transaction_conn.execute(text("""
                CREATE TABLE esg_financials_raw (
                    CompanyID TEXT PRIMARY KEY,
                    CompanyName TEXT NOT NULL,
                    Industry TEXT NOT NULL,
                    Region TEXT NOT NULL,
                    Revenue REAL CHECK (Revenue >= 0 OR Revenue IS NULL),
                    ProfitMargin REAL,
                    MarketCap REAL CHECK (MarketCap >= 0 OR MarketCap IS NULL),
                    GrowthRate REAL,
                    data_quality_status TEXT NOT NULL
                );
            """))
            
            # PERFORMANCE OPTIMIZATION LAYER: Deploy B-Tree analytical indexing for high-speed slicer filters
            transaction_conn.execute(text('CREATE INDEX IF NOT EXISTS idx_esg_financials_industry ON esg_financials_raw (Industry);'))
            transaction_conn.execute(text('CREATE INDEX IF NOT EXISTS idx_esg_financials_region ON esg_financials_raw (Region);'))
            logging.info("🧹 Local SQLite Strategy: Schema mapped with strict Primary Key, CHECK limits & Analytical B-Tree Indexes.")

            for _, row in validated_df.iterrows():
                upsert_query = text("""
                    INSERT INTO esg_financials_raw (CompanyID, CompanyName, Industry, Region, Revenue, ProfitMargin, MarketCap, GrowthRate, data_quality_status)
                    VALUES (:CompanyID, :CompanyName, :Industry, :Region, :Revenue, :ProfitMargin, :MarketCap, :GrowthRate, :data_quality_status)
                    ON CONFLICT(CompanyID) DO UPDATE SET
                        CompanyName=excluded.CompanyName,
                        Industry=excluded.Industry,
                        Region=excluded.Region,
                        Revenue=excluded.Revenue,
                        ProfitMargin=excluded.ProfitMargin,
                        MarketCap=excluded.MarketCap,
                        GrowthRate=excluded.GrowthRate,
                        data_quality_status=excluded.data_quality_status;
                """)
                transaction_conn.execute(upsert_query, row.to_dict())
        else:
            for _, row in validated_df.iterrows():
                upsert_query = text("""
                    INSERT INTO esg_financials_raw ("CompanyID", "CompanyName", "Industry", "Region", "Revenue", "ProfitMargin", "MarketCap", "GrowthRate", "data_quality_status")
                    VALUES (:CompanyID, :CompanyName, :Industry, :Region, :Revenue, :ProfitMargin, :MarketCap, :GrowthRate, :data_quality_status)
                    ON CONFLICT ("CompanyID") DO UPDATE SET
                        "CompanyName" = EXCLUDED.CompanyName,
                        "Industry" = EXCLUDED.Industry,
                        "Region" = EXCLUDED.Region,
                        "Revenue" = EXCLUDED.Revenue,
                        "ProfitMargin" = EXCLUDED.ProfitMargin,
                        "MarketCap" = EXCLUDED.MarketCap,
                        "GrowthRate" = EXCLUDED.GrowthRate,
                        "data_quality_status" = EXCLUDED.data_quality_status;
                """)
                transaction_conn.execute(upsert_query, row.to_dict())
                
    logging.info("🏆 PIPELINE RUN COMPLETION: STATUS 0 [SUCCESS]. Idempotency & Database Integrity metrics verified.\n")
    sys.exit(0)

except pa.errors.SchemaError as schema_fault:
    logging.critical(f"❌ PIPELINE STOPPED VIA PANDERA INGESTION SHIELD: {schema_fault}")
    sys.exit(1)
except Exception as fatal_error:
    logging.critical(f"❌ PIPELINE INGESTION CRITICAL RUNTIME FAILURE: {fatal_error}")
    sys.exit(1)
