# 📊 Corporate ESG & Financial Performance Analytics Pipeline

A self-directed data engineering and portfolio framework modeling the statistical relationship between corporate sustainability registries (**ESG Scores**) and actual market profitability. This pipeline processes an analytical dataset containing over **11,000 global corporate records**, implementing a self-healing cleaning architecture, declarative data schema validations, corporate observability logging handlers, automated cloud templates, and relational database SQL modeling.

## 🚀 Live Interactive Dashboard Preview
![ESG Financial Dashboard](dashboard_preview.gif)

---

## 🏗️ Architecture Design: Enterprise Observability & Self-Healing Layout
To maximize data product safety, engineering audit transparency, and repository reliability across cloud environments, the framework deploys a strict multi-layered verification and monitoring architecture:
1. **Enterprise Logging Framework (`logging`):** Completely replaced legacy, unmonitored standard stdout text prints with a formal Python logging machine. Events, environment shifts, and connection faults are systematically tracked across precise execution states (`INFO`, `WARNING`, `CRITICAL`) to allow direct parsing by automated cloud orchestrators.
2. **First-Class Rejection Metrics & Quarantine:** Malformed textual data corruptions or alphanumeric anomalies are proactively intercepted row-by-row. Instead of masking failures using silent zero conversions that skew corporate averages downstream, corrupt fields are cast to explicit `NULL` maps and actively tracked as a first-class operational quality metric.
3. **Automated Alerting Thresholds (Fail-Fast):** Incorporates an active runtime processing limit constraint. If the financial data ingestion pipeline encounters a critical row rejection rate greater than **5.0%** of the batch payload volume, the entire framework halts execution immediately and throws a hard termination state (`sys.exit(1)`) to trigger scheduler alerts.
4. **Self-Healing Pre-Load Layer:** Automatically coerces incoming data structure alignments (e.g., preventing Monday morning schema drift by casting corporate IDs to clean strings) and strips alphanumeric grouping text formatting before metrics conversion.
5. **Decoupled Unit Testing (`pytest`):** Core transformation math and ESG classification rules are fully decoupled into an independent logic module (`esg_parser.py`) to eliminate environmental connection dependencies, allowing rapid parameterized testing execution.
6. **Declarative Schema Validation (`pandera`):** Screens the fully aligned, cleaned, and healed dataframe for structural attributes, duplicate keys, and range constraints before allowing downstream relational loading.

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
- **Data Engineering:** Python (Pandas) executing an inline self-healing text cleanup matrix, robust `logging` stream handlers, and strict type formatting via `pandera.pandas`. High-precision accounting aggregates utilize `decimal.Decimal` logic to completely eliminate binary float drifting. Loose zero-interpolations (`.fillna(0)`) are entirely deprecated.
- **Testing Suite:** `pytest` executing parametrized, table-driven unit tests to simulate and intercept raw input anomalies.
- **Database Layer:** PostgreSQL object-relational cluster blueprint utilizing batch execution streams (`chunksize=10000`) and secure Connection Pooler configurations (Port `6543`), featuring automated local file backup routing.
- **BI Visualization:** Microsoft Power BI Desktop tailored with custom DAX data formatting measures and spacing layouts.

---

## 📁 Repository Directory Structure

```text
esg-financial-analytics/
│
├── company_esg_financial_dataset_sample.csv  # Custom Ingestion Sample Dataset
├── esg_parser.py                             # Pure Decoupled Parsing & Business Logic (100% Testable)
├── esg_analytics.py                          # Main Core Analytics Engine & Production Logging Handlers
├── esg_ingestion.py                          # Relational Storage Ingestion Stream with Logging Blueprint
├── test_esg.py                               # Parametrized Pytest Suite & Code Crash Simulator
├── requirements.txt                          # Locked Software Dependency Layout Matrix
└── README.md                                 # Enterprise Systems Documentation
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

### 3. Run the Local Financial Validation Audit Pipeline
Execute the main analytics script to process the local sample dataset and verify clean terminal metrics outputs:
```powershell
python esg_analytics.py
```

### 4. Inspect the Ingestion Architecture Blueprint
Test the dual-mode framework pipeline to inspect database ingestion scalability configurations:
```powershell
python esg_ingestion.py
```

---
*Engineered under the UpDataLogic Performance Framework for transparent, honest, and reproducible analytics pipelines.*
