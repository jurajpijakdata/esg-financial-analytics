# 📊 Corporate ESG & Financial Performance Analytics Pipeline

A self-directed data engineering and portfolio framework modeling the statistical relationship between corporate sustainability registries (**ESG Scores**) and actual market profitability. This pipeline processes an analytical dataset containing over **11,000 global corporate records**, implementing strict data normalization, automated cloud storage templates, and relational database SQL modeling.

## 🚀 Live Interactive Dashboard Preview
![ESG Financial Dashboard](dashboard_preview.gif)

---

## 🔗 Dataset Provenance & Reproducibility (Rule 5)
* **Dataset Scope:** 11,000 corporate financial logs scaling up to the active reporting calendar.
* **Open Disclosure:** To ensure compliance with the **Clone & Run Standard**, this public repository contains a lightweight test pool: **`company_esg_financial_dataset_sample.csv` (100 rows)**. Reviewers can execute the complete end-to-end analytics and architecture blueprints instantly without heavy system overhead.

---

## 🎯 Key Analytical Insights & Anomalies Discovered
By deploying robust type standardizations and strict data quality boundaries, the data pipeline isolates critical data-driven phenomena across major international trading blocs:

1. **The Sustainability Premium:** Corporations operating in the **ESG Leader** tier (ESG Score >= 75) demonstrate high operational efficiency, registering a peak **Average Profit Margin of 12.96%**.
2. **The Profitability Paradox:** Data cross-referencing validates a unique market anomaly — **ESG Laggards** (companies with sustainability markers under 40) command a slightly higher average profit margin than **ESG Average** companies. This margin spike is driven by zero-capital expenditure on environmental policy compliance, presenting a high-yield but volatile market vector.
3. **The Pollution Core:** Corporate top-line scale (`Revenue`) correlates directly with environmental footprints (`Carbon Emissions`), demonstrating a technical baseline requirement for predictive carbon-tax risk modeling layers.

---

## 🛠️ Tech Stack & Engineering Architecture
- **Data Engineering:** Python (Pandas) executing high-precision numeric vectoring via `decimal.Decimal` to eliminate fractional binary float drifting (`://30000000000000004.com`). Loose zero-interpolation methods (`.fillna(0)`) have been deprecated to protect downstream mathematical averages.
- **Database Layer:** PostgreSQL object-relational cluster blueprint utilizing batch execution streams (`chunksize=10000`) and secure Connection Pooler configurations (Port `6543`).
- **Semantic Modeling:** Cloud-based SQL Views utilizing dynamic lookup rules (`CASE WHEN` structures) to classify asset risk tiers.
- **Business Intelligence:** Microsoft Power BI Desktop tailored with custom DAX data formatting measures and spacing layouts.

---

## 📁 Repository Structure
* `esg_analytics.py`: Main analytics engine executing data extraction from local sample sets, high-precision type casting, data quality isolation, and mathematical aggregation verification.
* `esg_ingestion.py`: Dual-Mode Data Engineering Blueprint. Runs locally as a structural architecture concept for clients, but activates automatically into an online stream loader upon secure `.env` connection pooler target mapping.
* `requirements.txt`: Locked software dependency versions ensuring 100% reproducible cross-platform environments.

---

## 🔧 Database Layer Integration (SQL View)
To isolate corporate performance tiers dynamically without altering immutable raw transaction registries, the following production view layout was deployed:

```sql
CREATE OR REPLACE VIEW public.v_esg_investment_analytics AS
SELECT 
    "CompanyID" AS company_id,
    "CompanyName" AS company_name,
    "Industry" AS industry,
    "Region" AS region,
    "Year" AS reporting_year,
    "Revenue" AS revenue,
    "ProfitMargin" AS profit_margin,
    "MarketCap" AS market_cap,
    "ESG_Overall" AS esg_score,
    "CarbonEmissions" AS carbon_emissions,
    CASE 
        WHEN "ESG_Overall" >= 75 THEN 'ESG Leader (High Sustainability)'
        WHEN "ESG_Overall" >= 40 THEN 'ESG Average (Medium Sustainability)'
        ELSE 'ESG Laggard (Low Sustainability)'
    END AS esg_investment_tier,
    ("Revenue" * ("ProfitMargin" / 100.0)) AS net_profit_amount
FROM public.esg_financials_raw;
```

---

## 🚀 Quick Start (Clone & Run Standard)

### 1. Replicate the Dependencies Layout
Install standard Python dependencies inside your environment:
```powershell
pip install -r requirements.txt
```

### 2. Run the Local Validation Ingestion
Execute the main analytics script to process the local sample dataset and verify verified math output strings:
```powershell
python esg_analytics.py
```

### 3. Verify the Architecture Blueprint Ingestion
Test the dual-mode framework pipeline to inspect corporate ingestion scalability configurations:
```powershell
python esg_ingestion.py
```

---
*Engineered under the UpDataLogic Performance Framework for transparent, honest, and reproducible analytics pipelines.*
