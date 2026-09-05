import os
import sys
import logging
import pandas as pd
import pandera.pandas as pa
from pathlib import Path

# Import the decoupled tested business logic from our parser module
from esg_parser import clean_esg_numeric_vector

# =====================================================================
# ENTERPRISE LOGGING CONFIGURATION (Module 6 Standard)
# =====================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [UpDataLogic ESG Engine] - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logging.info("🚀 Starting UpDataLogic ESG & Financial Analytics Engine (Production Observability Mode)...")

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "company_esg_financial_dataset_sample.csv"

# First-class operation metrics trackers for alerting layers
METRICS_TRACKER = {
    "total_records_extracted": 0,
    "successfully_healed_records": 0,
    "rejected_records_critical": 0
}

# 1. DECLARATIVE DATA QUALITY SCHEMA SHIELD (Pandera Specification)
esg_data_schema = pa.DataFrameSchema({
    "CompanyID": pa.Column(str, nullable=False),
    "CompanyName": pa.Column(str, nullable=False),
    "Industry": pa.Column(str, nullable=False),
    "Region": pa.Column(str, nullable=False),
    "Revenue": pa.Column(float, nullable=True),
    "ProfitMargin": pa.Column(float, nullable=True),
    "MarketCap": pa.Column(float, nullable=True),
    "GrowthRate": pa.Column(float, nullable=True),
    "ESG_Overall": pa.Column(float, pa.Check.in_range(0, 100), nullable=True),
    "CarbonEmissions": pa.Column(float, nullable=True),
    "WaterUsage": pa.Column(float, nullable=True),
    "EnergyConsumption": pa.Column(float, nullable=True)
})

# DATA PIPELINE EXECUTION WITH DEFENSIVE MONITORING
try:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Critical data resource missing at targeted path: {DATA_FILE}")
        
    logging.info(f"📥 1. EXTRACTION: Loading raw corporate dataset from: {DATA_FILE.name}")
    df = pd.read_csv(DATA_FILE, dtype={"CompanyID": str}, low_memory=False)
    
    METRICS_TRACKER["total_records_extracted"] = len(df)
    logging.info(f"✅ EXTRACTION SUCCESS: Pulled {METRICS_TRACKER['total_records_extracted']:,} logs into high-performance dataframe memory.")
    
    logging.info("⏳ 2. TRANSFORMATION: Executing high-precision financial healing pipelines...")

    financial_columns = ['Revenue', 'ProfitMargin', 'MarketCap', 'GrowthRate', 'ESG_Overall']
    env_columns = ['CarbonEmissions', 'WaterUsage', 'EnergyConsumption']
    all_metrics = financial_columns + env_columns
    
    # Run data normalization row-by-row and extract anomalies to NULL mapping
    for column in all_metrics:
        df[f'{column}_Decimal_Obj'] = [clean_esg_numeric_vector(val) for val in df[column]]
        df[column] = df[f'{column}_Decimal_Obj'].apply(lambda x: float(x) if x is not None else None)
        
    # Calculate operational data quality status vector flags
    df['data_quality_status'] = df[all_metrics].isnull().any(axis=1).map({True: 'UNKNOWN', False: 'CLEAN'})
    
    # Track critical rejections as first-class output parameters
    METRICS_TRACKER["rejected_records_critical"] = int(df['ProfitMargin'].isna().sum())
    METRICS_TRACKER["successfully_healed_records"] = METRICS_TRACKER["total_records_extracted"] - METRICS_TRACKER["rejected_records_critical"]
        
    logging.info("🛡️ 3. VALIDATION: Running declarative structural data quality tests via Pandera schema evaluation...")
    validated_df = esg_data_schema.validate(df)
    
    rejection_rate = (METRICS_TRACKER["rejected_records_critical"] / METRICS_TRACKER["total_records_extracted"]) * 100
    logging.info(f"📊 DATA QUALITY METRICS: Clean/Healed: {METRICS_TRACKER['successfully_healed_records']:,} | Quarantined/NULL: {METRICS_TRACKER['rejected_records_critical']:,} ({rejection_rate:.2f}%)")
    
    # Alerting threshold constraints validation (Fail-fast principle rule)
    if rejection_rate > 5.0:
        raise ValueError(f"Pipeline execution aborted. Rejection rate {rejection_rate:.2f}% breached production threshold limit (5.0%)")
        
    logging.info("\n=== 📊 QUICK INSIGHT: AVG PROFIT MARGIN BY INDUSTRY (VERIFIED) ===")
    validated_df['ProfitMargin_Float'] = validated_df['ProfitMargin_Decimal_Obj'].astype(float)
    avg_margin = validated_df.groupby('Industry')['ProfitMargin_Float'].mean().sort_values(ascending=False)
    print(avg_margin)
    print("=" * 60)
    
    logging.info("🏆 PIPELINE PROCESS COMPLETION: STATUS 0 [SUCCESS]. Financial telemetry secured safely.\n")
    sys.exit(0) # Guarantee clean orchestrator exit status code parameters

except pa.errors.SchemaError as schema_fault:
    logging.critical(f"❌ PIPELINE STOPPED BY PANDERA STRUCTURAL SHIELD: {schema_fault}")
    sys.exit(1) # Enforce strict exit 1 flags for schedulers
except Exception as fatal_error:
    logging.critical(f"❌ PIPELINE CRITICAL RUNTIME FAILURE: {fatal_error}")
    sys.exit(1)
