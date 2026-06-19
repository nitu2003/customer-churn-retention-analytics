-- Power BI: churn KPI views (Import or DirectQuery)
-- Connect to these views in Power BI Desktop — do not use .pbix from repo

DROP VIEW IF EXISTS vw_pbi_churn_kpi_summary;
DROP VIEW IF EXISTS vw_pbi_churn_kpi_by_contract;
DROP VIEW IF EXISTS vw_pbi_churn_kpi_by_internet_service;
DROP VIEW IF EXISTS vw_pbi_churn_kpi_by_payment_method;
DROP VIEW IF EXISTS vw_pbi_churn_kpi_dimensions;

CREATE VIEW vw_pbi_churn_kpi_summary AS
SELECT * FROM vw_churn_kpi_summary;

CREATE VIEW vw_pbi_churn_kpi_by_contract AS
SELECT * FROM vw_churn_kpi_by_contract;

CREATE VIEW vw_pbi_churn_kpi_by_internet_service AS
SELECT * FROM vw_churn_kpi_by_internet_service;

CREATE VIEW vw_pbi_churn_kpi_by_payment_method AS
SELECT * FROM vw_churn_kpi_by_payment_method;

-- Single table for stacked bar / matrix (unpivot-friendly long format)
CREATE VIEW vw_pbi_churn_kpi_dimensions AS
SELECT dimension_name, dimension_value, total_customers, churned_customers, churn_rate_pct,
       total_monthly_revenue, churned_monthly_revenue
FROM vw_churn_kpi_by_contract
UNION ALL
SELECT dimension_name, dimension_value, total_customers, churned_customers, churn_rate_pct,
       total_monthly_revenue, churned_monthly_revenue
FROM vw_churn_kpi_by_internet_service
UNION ALL
SELECT dimension_name, dimension_value, total_customers, churned_customers, churn_rate_pct,
       total_monthly_revenue, churned_monthly_revenue
FROM vw_churn_kpi_by_payment_method;
