-- Tenure bucket analysis for retention and churn patterns

DROP VIEW IF EXISTS vw_tenure_bucket_summary;
DROP VIEW IF EXISTS vw_tenure_bucket_churn_detail;

CREATE VIEW vw_tenure_bucket_summary AS
SELECT
    b.tenure_bucket,
    b.tenure_bucket_sort,
    COUNT(*) AS customer_count,
    SUM(b.is_churned) AS churned_customers,
    SUM(1 - b.is_churned) AS active_customers,
    ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct,
    ROUND(AVG(b.tenure), 1) AS avg_tenure_months,
    ROUND(SUM(b.monthly_charges), 2) AS total_monthly_revenue,
    ROUND(SUM(b.churned_monthly_revenue), 2) AS churned_monthly_revenue,
    ROUND(SUM(b.at_risk_monthly_revenue), 2) AS at_risk_monthly_revenue
FROM vw_base_customers b
GROUP BY b.tenure_bucket, b.tenure_bucket_sort
ORDER BY b.tenure_bucket_sort;

CREATE VIEW vw_tenure_bucket_churn_detail AS
SELECT
    b.tenure_bucket,
    b.tenure_bucket_sort,
    b.contract,
    b.internet_service,
    COUNT(*) AS customer_count,
    SUM(b.is_churned) AS churned_customers,
    ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct,
    ROUND(SUM(b.monthly_charges), 2) AS total_monthly_revenue
FROM vw_base_customers b
GROUP BY
    b.tenure_bucket,
    b.tenure_bucket_sort,
    b.contract,
    b.internet_service
ORDER BY b.tenure_bucket_sort, churn_rate_pct DESC;
