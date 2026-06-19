-- Churn rate by customer segment (latest month)

CREATE OR REPLACE VIEW analytics.mart_churn_by_segment AS
WITH latest_month AS (
    SELECT MAX(snapshot_month) AS snapshot_month
    FROM analytics.fact_customer_monthly
)
SELECT
    c.segment,
    c.region,
    COUNT(*) AS customers,
    COUNT(*) FILTER (WHERE f.is_churned) AS churned,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE f.is_churned) / NULLIF(COUNT(*), 0),
        2
    ) AS churn_rate_pct,
    SUM(f.mrr) FILTER (WHERE f.is_churned) AS churned_mrr
FROM analytics.fact_customer_monthly f
INNER JOIN staging.dim_customer c ON f.customer_id = c.customer_id
CROSS JOIN latest_month lm
WHERE f.snapshot_month = lm.snapshot_month
GROUP BY c.segment, c.region
ORDER BY churn_rate_pct DESC;
