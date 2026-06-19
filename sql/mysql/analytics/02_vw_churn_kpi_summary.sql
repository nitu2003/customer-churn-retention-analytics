-- Portfolio-level churn KPIs (single-row summary for dashboard cards)

DROP VIEW IF EXISTS vw_churn_kpi_summary;

CREATE VIEW vw_churn_kpi_summary AS
SELECT
    COUNT(*) AS total_customers,
    SUM(b.is_churned) AS churned_customers,
    SUM(1 - b.is_churned) AS active_customers,
    ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct,
    ROUND(100.0 * SUM(1 - b.is_churned) / NULLIF(COUNT(*), 0), 2) AS retention_rate_pct,
    ROUND(SUM(b.monthly_charges), 2) AS total_monthly_revenue,
    ROUND(SUM(b.retained_monthly_revenue), 2) AS retained_monthly_revenue,
    ROUND(SUM(b.churned_monthly_revenue), 2) AS churned_monthly_revenue,
    ROUND(SUM(b.at_risk_monthly_revenue), 2) AS at_risk_monthly_revenue,
    ROUND(AVG(b.monthly_charges), 2) AS avg_monthly_charges,
    ROUND(AVG(CASE WHEN b.is_churned = 1 THEN b.monthly_charges END), 2) AS avg_churned_monthly_charges,
    ROUND(AVG(CASE WHEN b.is_churned = 0 THEN b.monthly_charges END), 2) AS avg_active_monthly_charges,
    ROUND(AVG(b.tenure), 1) AS avg_tenure_months,
    ROUND(AVG(CASE WHEN b.is_churned = 1 THEN b.tenure END), 1) AS avg_churned_tenure_months,
    ROUND(AVG(CASE WHEN b.is_churned = 0 THEN b.tenure END), 1) AS avg_active_tenure_months
FROM vw_base_customers b;
