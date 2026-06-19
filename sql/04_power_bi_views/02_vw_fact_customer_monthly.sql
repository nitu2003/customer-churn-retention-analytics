-- Power BI: monthly snapshot fact (join to dim_customer and date table)

CREATE OR REPLACE VIEW bi.vw_fact_customer_monthly AS
SELECT
    f.customer_id,
    f.snapshot_month,
    f.snapshot_month AS snapshot_date,
    f.is_active,
    f.is_churned,
    f.mrr,
    f.usage_score,
    f.tenure_months,
    c.segment,
    c.region,
    c.signup_cohort_month
FROM analytics.fact_customer_monthly f
LEFT JOIN bi.vw_dim_customer c ON f.customer_id = c.customer_id;
