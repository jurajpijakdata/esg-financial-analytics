# 📊 Corporate ESG & Financial Performance Analytics Pipeline

A self-directed data engineering and portfolio framework modeling the statistical relationship between corporate sustainability registries (**ESG Scores**) and actual market profitability. This pipeline processes an analytical dataset containing over **11,000 global corporate records**, implementing a self-healing cleaning architecture, declarative data schema validations, automated cloud templates, and relational database SQL modeling.

## 🚀 Live Interactive Dashboard Preview
![ESG Financial Dashboard](dashboard_preview.gif)

---

## 🏗️ Architecture Design: Self-Healing & Automated Verification Layout
To maximize data product safety and project robustness across active enterprise reporting schedules, the framework deploys a strict multi-layered engineering and validation layout:
1. **Self-Healing Pre-Load Layer:** Automatically coerces incoming data structure alignments (e.g., preventing Monday morning schema drift by casting corporate IDs to clean strings) and strips alphanumeric grouping text formatting before metrics conversion.
2. **Automated Unit Testing (`pytest`):** Core transformation algorithms are fully decoupled into pure isolated functions, verified against table-driven test vectors, edge-case numeric parameters, and structural data noise inputs.
3. **Declarative Schema Validation (`pandera`):** The ingestion pipeline is armed with a strict semantic quality schema layer. It screens records for missing attributes (`Null`), duplicate flags, boundary ranges, and structural typing variations before writing records downstream.

---

## 🔗 Dataset Provenance & Disclosure (Clone & Run Standard)
* **Dataset Scope:** 11,000 corporate financial logs scaling up to the active reporting calendar.
* **Open Disclosure:** To ensure compliance with the **Clone & Run Standard**, this public repository contains a lightweight test validation pool: **`company_esg_financial_dataset_sample.csv` (100 rows)**. Reviewers and target clients can execute the end-to-end analytics and architecture blueprints instantly without heavy system processing overhead.

---

## 🎯 Key Analytical Insights & Anomalies Discovered
By deploying robust type standardizations and strict data quality boundaries, the data pipeline isolates critical data-driven phenomena across major international trading blocs:

1. **The Sustainability Premium:** Corporations operating in the **ESG Leader** tier (ESG Score >= 75) demonstrate high operational efficiency, registering a peak **Average Profit Margin of 12.96%**.
2. **The Profitability Paradox:** Data cross-referencing validates a unique market anomaly — **ESG Laggards** (companies with sustainability markers under 40) command a slightly higher average profit margin than **ESG Average** companies. This margin spike is driven by zero-capital expenditure on environmental policy compliance, presenting a high-yield but volatile market vector.
3. **The Pollution Core:** Corporate top-line scale (`Revenue`) correlates directly with environmental footprints (`Carbon Emissions`), demonstrating a technical baseline requirement for predictive carbon-tax risk modeling layers.

---

## 🛠️ Tech Stack & Pipeline Configurations
- **Data Engineering:** Python (Pandas) executing an inline self-healing text cleanup matrix and strict type formatting via `pandera.pandas`. High-precision accounting aggregates utilize `decimal.Decimal` logic to completely eliminate binary float drifting. Loose zero-interpolations (`.fillna(0)`) are entirely deprecated.
- **Testing Suite:** `pytest` executing parametrized, table-driven unit tests to simulate and intercept raw input anomalies.
- **Database Layer:** PostgreSQL object-relational cluster blueprint utilizing batch execution streams (`chunksize=10000`) and secure Connection Pooler configurations (Port `6543`), featuring automated local file backup routing.
- **BI Visualization:** Microsoft Power BI Desktop tailored with custom DAX data formatting measures and spacing layouts.

---

## 📁 Repository Directory Structure

```text
esg-financial-analytics/
│
├── company_esg_financial_dataset_sample.csv  # Custom Ingestion Sample Dataset
├── esg_analytics.py                         # Main Core Analytics Engine & Pandera Shield Verification
├── esg_ingestion.py                         # Relational Storage Ingestion Stream Blueprint
├── test_esg.py                              # Automated Pytest Suite & Code Crash Simulator
├── requirements.txt                         # Locked Reproducible Software Dependency Layout
└── README.md                                # Enterprise Systems Documentation
```

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
Install standard Python dependencies inside your local execution environment:
```powershell
pip install -r requirements.txt
```

### 2. Execute Automated Code Testing
Run the complete unit testing suite using the built-in crash-test vectors to verify validation stability:
```powershell
pytest test_esg.py -v
```

### 3. Run the Local Validation Ingestion Pipeline
Execute the main analytics script to process the local sample dataset and verify clean terminal metrics outputs:
```powershell
python esg_analytics.py
```

### 4. Verify the Architecture Ingestion Blueprint
Test the dual-mode framework pipeline to inspect corporate ingestion scalability configurations:
```powershell
python esg_ingestion.py
```

---
*Engineered under the UpDataLogic Performance Framework for transparent, honest, and reproducible analytics pipelines.*
