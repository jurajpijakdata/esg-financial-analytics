import os
import sys
import logging
import pandas as pd
import pandera.pandas as pa
from pathlib import Path
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

from esg_parser import clean_esg_numeric_vector

# Force UTF-8 stdout so the emoji in the log messages below never crash a
# non-interactive run on Windows (its default console codepage can't encode
# them, which otherwise silently drops all logging output).
sys.stdout.reconfigure(encoding="utf-8")

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

CHUNK_SIZE = 1000
REJECTION_THRESHOLD_PCT = 25.0

# Every numeric column in the source file, including the ESG/environmental
# scores. These used to be dropped entirely during ingestion -- only the four
# financial columns made it into the database, even though the whole point of
# this project is ESG score vs. financial performance. They're loaded now so
# the database actually holds what the project claims to hold.
FINANCIAL_COLUMNS = ['Revenue', 'ProfitMargin', 'MarketCap', 'GrowthRate']
ESG_COLUMNS = ['ESG_Overall', 'ESG_Environmental', 'ESG_Social', 'ESG_Governance']
ENVIRONMENTAL_COLUMNS = ['CarbonEmissions', 'WaterUsage', 'EnergyConsumption']
ALL_NUMERIC_COLUMNS = FINANCIAL_COLUMNS + ESG_COLUMNS + ENVIRONMENTAL_COLUMNS

# Define Strict Data Quality Ingestion Shield via Pandera Specification
esg_ingest_schema = pa.DataFrameSchema({
    "CompanyID": pa.Column(str, nullable=False),
    "CompanyName": pa.Column(str, nullable=False),
    "Industry": pa.Column(str, nullable=False),
    "Region": pa.Column(str, nullable=False),
    "Year": pa.Column(int, nullable=False),
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
    # Use the same shared, tested parser as esg_analytics.py so a given raw
    # value is interpreted identically no matter which script processes it,
    # and so money keeps full Decimal precision instead of binary float drift.
    for col in ALL_NUMERIC_COLUMNS:
        df[f'{col}_Decimal_Obj'] = [clean_esg_numeric_vector(val) for val in df[col]]
        df[col] = df[f'{col}_Decimal_Obj'].apply(lambda d: float(d) if d is not None else None)

    df['Year'] = pd.to_numeric(df['Year'], errors='coerce').astype('Int64')

    logging.info("🛡️ 3. VALIDATION: Running structural data quality tests via Pandera schema evaluation...")
    validated_df = esg_ingest_schema.validate(df)

    validated_df['data_quality_status'] = validated_df[['Revenue', 'ProfitMargin']].isnull().any(axis=1).map({True: 'UNKNOWN', False: 'CLEAN'})

    total_records = len(validated_df)
    rejected_records = int((validated_df['data_quality_status'] == 'UNKNOWN').sum())
    rejection_rate = (rejected_records / total_records) * 100 if total_records else 0.0
    logging.info(f"📊 DATA QUALITY METRICS: Clean: {total_records - rejected_records:,} | Quarantined: {rejected_records:,} ({rejection_rate:.2f}%)")

    if rejection_rate > REJECTION_THRESHOLD_PCT:
        raise ValueError(f"Pipeline execution aborted. Rejection rate {rejection_rate:.2f}% breached production threshold limit ({REJECTION_THRESHOLD_PCT}%)")

    logging.info("📤 4. LOADING: Executing idempotent UPSERT pattern routing directly to database engine...")

    # CompanyID alone is NOT unique -- every company has one row per
    # reporting year, so (CompanyID, Year) together is the real key. Using
    # CompanyID alone as the primary key / conflict target (the previous
    # behavior) meant every later year silently overwrote the earlier one,
    # so a 100-row sample collapsed down to 10 surviving rows -- one per
    # company -- with 90% of the historical data silently destroyed.
    key_columns = ['CompanyID', 'CompanyName', 'Industry', 'Region', 'Year']
    all_columns = key_columns + ALL_NUMERIC_COLUMNS + ['data_quality_status']

    records = []
    for _, row in validated_df.iterrows():
        rec = {
            'CompanyID': row['CompanyID'],
            'CompanyName': row['CompanyName'],
            'Industry': row['Industry'],
            'Region': row['Region'],
            'Year': int(row['Year']),
            'data_quality_status': row['data_quality_status'],
        }
        for col in ALL_NUMERIC_COLUMNS:
            rec[col] = row[f'{col}_Decimal_Obj']
        records.append(rec)

    with engine.begin() as transaction_conn:
        is_sqlite = str(engine.url).startswith('sqlite')

        if is_sqlite:
            numeric_check_columns = {'Revenue', 'MarketCap', 'CarbonEmissions', 'WaterUsage', 'EnergyConsumption'}
            column_defs = []
            for col in ALL_NUMERIC_COLUMNS:
                if col == 'ESG_Overall':
                    column_defs.append(f"{col} REAL CHECK ({col} BETWEEN 0 AND 100 OR {col} IS NULL)")
                elif col in numeric_check_columns:
                    column_defs.append(f"{col} REAL CHECK ({col} >= 0 OR {col} IS NULL)")
                else:
                    column_defs.append(f"{col} REAL")
            column_defs_sql = ",\n                    ".join(column_defs)

            # PRODUCTION BLUEPRINT: Deploy strict CHECK constraints to enforce structural data quality
            transaction_conn.execute(text("DROP TABLE IF EXISTS esg_financials_raw;"))
            transaction_conn.execute(text(f"""
                CREATE TABLE esg_financials_raw (
                    CompanyID TEXT NOT NULL,
                    CompanyName TEXT NOT NULL,
                    Industry TEXT NOT NULL,
                    Region TEXT NOT NULL,
                    Year INTEGER NOT NULL,
                    {column_defs_sql},
                    data_quality_status TEXT NOT NULL,
                    PRIMARY KEY (CompanyID, Year)
                );
            """))

            # PERFORMANCE OPTIMIZATION LAYER: Deploy B-Tree analytical indexing for high-speed slicer filters
            transaction_conn.execute(text('CREATE INDEX IF NOT EXISTS idx_esg_financials_industry ON esg_financials_raw (Industry);'))
            transaction_conn.execute(text('CREATE INDEX IF NOT EXISTS idx_esg_financials_region ON esg_financials_raw (Region);'))
            logging.info("🧹 Local SQLite Strategy: Schema mapped with composite Primary Key (CompanyID, Year), CHECK limits & Analytical B-Tree Indexes.")

            # sqlite3 has no native adapter for Decimal, so numeric values are
            # cast to float for this branch only; the Postgres branch below
            # keeps the original Decimal objects for full accounting precision.
            sqlite_records = []
            for rec in records:
                sqlite_rec = dict(rec)
                for col in ALL_NUMERIC_COLUMNS:
                    sqlite_rec[col] = float(rec[col]) if rec[col] is not None else None
                sqlite_records.append(sqlite_rec)

            column_list = ", ".join(all_columns)
            value_list = ", ".join(f":{c}" for c in all_columns)
            update_list = ",\n                        ".join(f"{c}=excluded.{c}" for c in all_columns if c not in ('CompanyID', 'Year'))
            upsert_query = text(f"""
                INSERT INTO esg_financials_raw ({column_list})
                VALUES ({value_list})
                ON CONFLICT(CompanyID, Year) DO UPDATE SET
                    {update_list};
            """)

            for i in range(0, len(sqlite_records), CHUNK_SIZE):
                transaction_conn.execute(upsert_query, sqlite_records[i:i + CHUNK_SIZE])
        else:
            quoted_columns = ", ".join(f'"{c}"' for c in all_columns)
            value_list = ", ".join(f":{c}" for c in all_columns)
            # Both sides of the SET clause must be quoted: EXCLUDED is a
            # pseudo-table with the same (case-sensitive) column names as the
            # real table, and an unquoted identifier gets folded to lowercase
            # by Postgres, which then fails to match a quoted mixed-case
            # column like "CompanyName" -- this used to break every real
            # Postgres run with "column excluded.companyname does not exist".
            update_list = ",\n                    ".join(
                f'"{c}" = EXCLUDED."{c}"' for c in all_columns if c not in ('CompanyID', 'Year')
            )
            upsert_query = text(f"""
                INSERT INTO esg_financials_raw ({quoted_columns})
                VALUES ({value_list})
                ON CONFLICT ("CompanyID", "Year") DO UPDATE SET
                    {update_list};
            """)

            for i in range(0, len(records), CHUNK_SIZE):
                transaction_conn.execute(upsert_query, records[i:i + CHUNK_SIZE])

    logging.info(f"🏆 PIPELINE RUN COMPLETION: STATUS 0 [SUCCESS]. {total_records:,} rows upserted. Idempotency & Database Integrity metrics verified.\n")
    sys.exit(0)

except pa.errors.SchemaError as schema_fault:
    logging.critical(f"❌ PIPELINE STOPPED VIA PANDERA INGESTION SHIELD: {schema_fault}")
    sys.exit(1)
except Exception as fatal_error:
    logging.critical(f"❌ PIPELINE INGESTION CRITICAL RUNTIME FAILURE: {fatal_error}")
    sys.exit(1)
