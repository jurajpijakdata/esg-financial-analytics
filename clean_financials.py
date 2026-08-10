import pandas as pd

# Define the dataset path directly in the main folder
file_path = 'company_esg_financial_dataset.csv'

try:
    print("1. Loading ESG financial dataset...")
    df = pd.read_csv(file_path, low_memory=False)
    
    print("\n2. Checking for missing values (NaN)...")
    # Count missing values in key analytical columns
    missing_data = df[['Revenue', 'ProfitMargin', 'MarketCap', 'ESG_Overall']].isnull().sum()
    print(missing_data)
    
    print("\n3. Executing strict data cleansing pipeline...")
    # Convert financial metrics to numeric, replacing any corrupt text with 0
    financial_columns = ['Revenue', 'ProfitMargin', 'MarketCap', 'GrowthRate', 'ESG_Overall']
    for column in financial_columns:
        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)
        
    # Convert environmental metrics to numeric
    env_columns = ['CarbonEmissions', 'WaterUsage', 'EnergyConsumption']
    for column in env_columns:
        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)
        
    print("\n=== 🎉 DATA CLEANSING COMPLETED SUCCESSFULLY ===")
    print(f"Cleaned dataset rows: {df.shape[0]:,}")
    print(f"Cleaned dataset columns: {df.shape[1]}")
    
    # Quick business proof: print average profit margin by Industry
    print("\n=== 📊 QUICK INSIGHT: AVG PROFIT MARGIN BY INDUSTRY ===")
    avg_margin = df.groupby('Industry')['ProfitMargin'].mean().sort_values(ascending=False)
    print(avg_margin)

except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found in the root folder. Please verify the filename.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
