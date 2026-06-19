-- Churn KPIs broken down by key business dimensions

DROP VIEW IF EXISTS vw_churn_kpi_by_contract;
DROP VIEW IF EXISTS vw_churn_kpi_by_internet_service;
DROP VIEW IF EXISTS vw_churn_kpi_by_payment_method;

CREATE VIEW vw_churn_kpi_by_contract AS
SELECT
    'contract' AS dimension_name,
    b.contract AS dimension_value,
    COUNT(*) AS total_customers,
    SUM(b.is_churned) AS churned_customers,
    ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct,
    ROUND(SUM(b.monthly_charges), 2) AS total_monthly_revenue,
    ROUND(SUM(b.churned_monthly_revenue), 2) AS churned_monthly_revenue
FROM vw_base_customers b
GROUP BY b.contract;

CREATE VIEW vw_churn_kpi_by_internet_service AS
SELECT
    'internet_service' AS dimension_name,
    b.internet_service AS dimension_value,
    COUNT(*) AS total_customers,
    SUM(b.is_churned) AS churned_customers,
    ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct,
    ROUND(SUM(b.monthly_charges), 2) AS total_monthly_revenue,
    ROUND(SUM(b.churned_monthly_revenue), 2) AS churned_monthly_revenue
FROM vw_base_customers b
GROUP BY b.internet_service;

CREATE VIEW vw_churn_kpi_by_payment_method AS
SELECT
    'payment_method' AS dimension_name,
    b.payment_method AS dimension_value,
    COUNT(*) AS total_customers,
    SUM(b.is_churned) AS churned_customers,
    ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct,
    ROUND(SUM(b.monthly_charges), 2) AS total_monthly_revenue,
    ROUND(SUM(b.churned_monthly_revenue), 2) AS churned_monthly_revenue
FROM vw_base_customers b
GROUP BY b.payment_method;
