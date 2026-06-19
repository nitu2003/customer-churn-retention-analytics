-- Revenue at risk: portfolio summary, risk bands, and customer-level detail

DROP VIEW IF EXISTS vw_revenue_at_risk_summary;
DROP VIEW IF EXISTS vw_revenue_at_risk_by_band;
DROP VIEW IF EXISTS vw_revenue_at_risk_customers;

CREATE VIEW vw_revenue_at_risk_summary AS
SELECT
    ROUND(SUM(b.monthly_charges), 2) AS total_monthly_revenue,
    ROUND(SUM(b.churned_monthly_revenue), 2) AS realized_churn_revenue_loss,
    ROUND(SUM(b.at_risk_monthly_revenue), 2) AS prospective_at_risk_revenue,
    ROUND(
        100.0 * SUM(b.churned_monthly_revenue) / NULLIF(SUM(b.monthly_charges), 0),
        2
    ) AS churned_revenue_share_pct,
    ROUND(
        100.0 * SUM(b.at_risk_monthly_revenue) / NULLIF(SUM(b.monthly_charges), 0),
        2
    ) AS at_risk_revenue_share_pct,
    SUM(CASE WHEN b.is_churned = 0 AND b.contract = 'Month-to-month' THEN 1 ELSE 0 END) AS at_risk_customer_count,
    SUM(CASE WHEN b.is_churned = 1 THEN 1 ELSE 0 END) AS churned_customer_count
FROM vw_base_customers b;

CREATE VIEW vw_revenue_at_risk_by_band AS
SELECT
    b.churn_risk_band,
    COUNT(*) AS customer_count,
    SUM(b.is_churned) AS churned_customers,
    ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct,
    ROUND(SUM(b.monthly_charges), 2) AS total_monthly_revenue,
    ROUND(SUM(b.at_risk_monthly_revenue), 2) AS at_risk_monthly_revenue,
    ROUND(SUM(b.churned_monthly_revenue), 2) AS churned_monthly_revenue
FROM vw_base_customers b
GROUP BY b.churn_risk_band
ORDER BY FIELD(b.churn_risk_band, 'High', 'Medium', 'Low');

CREATE VIEW vw_revenue_at_risk_customers AS
SELECT
    b.customer_id,
    b.customer_status,
    b.churn_risk_band,
    b.contract,
    b.internet_service,
    b.payment_method,
    b.tenure,
    b.tenure_bucket,
    b.monthly_charges,
    b.at_risk_monthly_revenue,
    b.churned_monthly_revenue,
    b.is_churned
FROM vw_base_customers b
WHERE b.is_churned = 1
   OR (b.is_churned = 0 AND b.churn_risk_band IN ('High', 'Medium'))
ORDER BY b.at_risk_monthly_revenue DESC, b.churned_monthly_revenue DESC;
