-- Monthly churn KPI mart

CREATE OR REPLACE VIEW analytics.mart_churn_monthly AS
SELECT
    snapshot_month,
    COUNT(*) AS customer_count,
    COUNT(*) FILTER (WHERE is_churned) AS churned_count,
    COUNT(*) FILTER (WHERE is_active) AS active_count,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE is_churned)
        / NULLIF(COUNT(*), 0),
        2
    ) AS churn_rate_pct,
    SUM(mrr) FILTER (WHERE is_active) AS active_mrr,
    SUM(mrr) FILTER (WHERE is_churned) AS churned_mrr
FROM analytics.fact_customer_monthly
GROUP BY snapshot_month
ORDER BY snapshot_month;
