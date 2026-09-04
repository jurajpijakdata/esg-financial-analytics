import os
import sys
import pandas as pd
import pandera.pandas as pa
from pathlib import Path
from decimal import Decimal, InvalidOperation

print("🚀 Starting UpDataLogic ESG & Financial Analytics Engine (Self-Healing & Validated)...")

# =====================================================================
# DYNAMIC PATH RESOLUTION
# =====================================================================
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "company_esg_financial_dataset_sample.csv"

# =====================================================================
# 1. DECLARATIVE DATA QUALITY SCHEMA (Ultimate Safety Validation)
# =====================================================================
esg_data_schema = pa.DataFrameSchema({
    "CompanyID": pa.Column(str, nullable=False), # Verified to be pure string text
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

# =====================================================================
# DATA PIPELINE EXECUTION
# =====================================================================
try:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Critical data resource missing at targeted path: {DATA_FILE}")
        
    print(f"📥 Loading raw dataset: {DATA_FILE.name}...")
    
    # KROK 1: SAMOOPRAVA NAČÍTANIA – automaticky opravíme typ stĺpca CompanyID na text (str),
    # aj keby ho v pondelok ráno poslal klient v CSV ako čisté celé čísla!
    df = pd.read_csv(DATA_FILE, dtype={"CompanyID": str}, low_memory=False)
    
    print("⏳ Executing high-precision corporate data healing layer...")
    
    # Samoopravná funkcia: automaticky vymaže tisíckové čiarky a opraví formát čísla z textu
    def self_heal_numeric_text(value):
        if pd.isna(value) or str(value).strip() == '':
            return None
        
        # Automatické odstraňovanie tisíckových čiarok a oprava desatinných bodiek
        clean_str = str(value).strip()
        if ',' in clean_str and '.' in clean_str:
            clean_str = clean_str.replace(',', '')
        elif ',' in clean_str and '.' not in clean_str:
            clean_str = clean_str.replace(',', '.')
            
        try:
            return Decimal(clean_str)
        except InvalidOperation:
            return None # Ak je text totálne zničený, vráti None, aby to neskreslilo priemery nulkami

    financial_columns = ['Revenue', 'ProfitMargin', 'MarketCap', 'GrowthRate', 'ESG_Overall']
    env_columns = ['CarbonEmissions', 'WaterUsage', 'EnergyConsumption']
    all_metrics = financial_columns + env_columns
    
    # KROK 2: SAMOOPRAVA ČÍSELNÝCH STĹPCOV – preženieme všetky metriky cez náš samoopravný proces,
    # čím Pandas donútime bezpečne načítať číselné hodnoty aj s textovými preklepmi
    for column in all_metrics:
        # Vytvoríme vysokopresnú objektovú vrstvu pre bezpečné výpočty bez driftovania floatov
        df[f'{column}_Decimal_Obj'] = df[column].apply(self_heal_numeric_text)
        # Vytvoríme float verziu pre štrukturálnu Pandera schému a Power BI reporting
        df[column] = df[f'{column}_Decimal_Obj'].apply(lambda x: float(x) if x is not None else None)
        
    print("🛡️ Running declarative data quality checks via Pandera schema evaluation...")
    # Pandera overí už našu automaticky opravenú a zrovnanú tabuľku
    validated_df = esg_data_schema.validate(df)
    
    # Izolácia neopraviteľných poškodených riadkov do kvalitatívneho vektora
    validated_df['data_quality_status'] = validated_df[all_metrics].isnull().any(axis=1).map({True: 'UNKNOWN', False: 'CLEAN'})
    
    print("\n=== 🎉 DATA VALIDATION & CLEANSING COMPLETED SUCCESSFULLY ===")
    print(f"Processed Rows: {validated_df.shape[0]:,}")
    
    print("\n=== 📊 QUICK INSIGHT: AVG PROFIT MARGIN BY INDUSTRY (VERIFIED) ===")
    validated_df['ProfitMargin_Float'] = validated_df['ProfitMargin_Decimal_Obj'].astype(float)
    avg_margin = validated_df.groupby('Industry')['ProfitMargin_Float'].mean().sort_values(ascending=False)
    print(avg_margin)
    
    print("\n🏆 ANALYTICS RUN COMPLETED SUCCESSFULLY.")

except pa.errors.SchemaError as schema_fault:
    print(f"\n❌ DATA QUALITY BREACH DETECTED BY PANDERA:\n{schema_fault}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"\n❌ PIPELINE CRITICAL FAILURE: {e}", file=sys.stderr)
    sys.exit(1)
