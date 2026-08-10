import pandas as pd
from sqlalchemy import create_engine

file_path = 'company_esg_financial_dataset.csv'
# Our verified local connection string to your PostgreSQL
db_url = 'postgresql+psycopg2://postgres:postgres01@localhost:5432/postgres'

try:
    print("1. Loading and cleaning data before database upload...")
    df = pd.read_csv(file_path, low_memory=False)
    
    # Quick standard cleaning layout
    all_numeric = [
        'Revenue', 'ProfitMargin', 'MarketCap', 'GrowthRate', 
        'ESG_Overall', 'CarbonEmissions', 'WaterUsage', 'EnergyConsumption'
    ]
    for col in all_numeric:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
    print("2. Connecting to PostgreSQL server...")
    engine = create_engine(db_url)
    
    print("3. Uploading financial data into 'esg_financials_raw' table...")
    # Using smooth chunks to ensure stability
    df.to_sql('esg_financials_raw', engine, schema='public', if_exists='replace', index=False, chunksize=10000)
    
    print("\n=== 🎉 SUCCESS! ALL ESG FINANCIAL DATA UPLOADED TO POSTGRESQL ===")

except Exception as e:
    print(f"\nDatabase Error: {e}")
