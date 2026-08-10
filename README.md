# 📊 Corporate ESG & Financial Performance Analytics Pipeline

An advanced end-to-end data engineering and business intelligence solution that analyzes the relationship between corporate sustainability indices (**ESG Scores**) and true market profitability across over **11,000 global corporations** up to **2025/2026**.

## 🚀 Live Interactive Dashboard Preview
![ESG Financial Dashboard](dashboard_preview.gif)

---

## 🎯 Key Executive Insights & Anomalies Discovered

By conducting exploratory data analysis (EDA) in JupyterLab and developing structural database layers, we uncovered critical investment patterns for the fund:

1. **The Sustainability Premium:** Companies classified as **ESG Leaders** (ESG Score >= 75) dominate the market with the highest efficiency, achieving a peak **Average Profit Margin of 12.96%**.
2. **The Profitability Paradox:** A fascinating market anomaly was proven — **ESG Laggards** (companies with low sustainability scores under 40) maintain a slightly higher average profit margin than **ESG Average** companies. This is driven by their zero-capital expenditure on green compliance, posing a high-yield but high-risk scenario for investors.
3. **The Pollution Core:** High-volume revenue engines (`Revenue (USD)`) scale directly with environmental impact (`Carbon Emissions (Tons)`), highlighting the urgent need for carbon-tax predictive risk modeling.

---

## 🛠️ Modern Data Stack Architecture

- **Data Engineering:** Python (Pandas) for strict data type standardizations and numerical `.fillna(0)` curing.
- **Database Layer:** PostgreSQL object-relational storage with optimized `chunksize=10000` batch streaming.
- **Business Logic Layer:** Permanent SQL Views utilizing advanced conditional mapping (`CASE WHEN` queries).
- **Business Intelligence:** Microsoft Power BI Desktop featuring customized DAX financial measures and premium executive layout spacing.

---

## 🔧 Database Layer Integration (SQL View)

To isolate investment risk tiers dynamically without altering raw production tables, the following permanent analytics layer was engineered:

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

## 💼 Total Portfolio Impact
This pipeline provides hedge fund managers with an unmanipulated, data-driven framework to optimize portfolio allocation, balancing corporate ethical standards against raw net profit margins.
