-- =====================================================================
-- CORPORATE ESG & FINANCIAL PERFORMANCE ANALYTICS - DATABASE SCHEMA
-- =====================================================================
-- Run this once against a fresh Postgres/Supabase database before
-- pointing esg_ingestion.py at it with real credentials. The table below
-- matches exactly what esg_ingestion.py writes to, and what the
-- v_esg_investment_analytics view further down reads from.
--
-- The primary key is (CompanyID, Year), not CompanyID alone: this dataset
-- has one row per company per reporting year, so CompanyID by itself is
-- not unique. A single-column CompanyID key would silently overwrite
-- every earlier year with the latest one on each upsert.

CREATE TABLE IF NOT EXISTS public.esg_financials_raw (
    "CompanyID" TEXT NOT NULL,
    "CompanyName" TEXT NOT NULL,
    "Industry" TEXT NOT NULL,
    "Region" TEXT NOT NULL,
    "Year" INTEGER NOT NULL,
    "Revenue" NUMERIC(18, 4) CHECK ("Revenue" >= 0 OR "Revenue" IS NULL),
    "ProfitMargin" NUMERIC(18, 4),
    "MarketCap" NUMERIC(18, 4) CHECK ("MarketCap" >= 0 OR "MarketCap" IS NULL),
    "GrowthRate" NUMERIC(18, 4),
    "ESG_Overall" NUMERIC(18, 4) CHECK ("ESG_Overall" BETWEEN 0 AND 100 OR "ESG_Overall" IS NULL),
    "ESG_Environmental" NUMERIC(18, 4),
    "ESG_Social" NUMERIC(18, 4),
    "ESG_Governance" NUMERIC(18, 4),
    "CarbonEmissions" NUMERIC(18, 4) CHECK ("CarbonEmissions" >= 0 OR "CarbonEmissions" IS NULL),
    "WaterUsage" NUMERIC(18, 4) CHECK ("WaterUsage" >= 0 OR "WaterUsage" IS NULL),
    "EnergyConsumption" NUMERIC(18, 4) CHECK ("EnergyConsumption" >= 0 OR "EnergyConsumption" IS NULL),
    "data_quality_status" TEXT NOT NULL DEFAULT 'CLEAN',

    CONSTRAINT pk_esg_financials_raw PRIMARY KEY ("CompanyID", "Year")
);

CREATE INDEX IF NOT EXISTS idx_esg_financials_industry ON public.esg_financials_raw ("Industry");
CREATE INDEX IF NOT EXISTS idx_esg_financials_region ON public.esg_financials_raw ("Region");
CREATE INDEX IF NOT EXISTS idx_esg_financials_year ON public.esg_financials_raw ("Year");

-- =====================================================================
-- REPORTING VIEW
-- =====================================================================
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

-- =====================================================================
-- ROW-LEVEL SECURITY
-- =====================================================================
ALTER TABLE public.esg_financials_raw ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Authenticated read access" ON public.esg_financials_raw;
CREATE POLICY "Authenticated read access" ON public.esg_financials_raw
    FOR SELECT TO authenticated USING (true);
