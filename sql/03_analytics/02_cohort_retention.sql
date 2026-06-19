-- Cohort retention: % of customers still active N months after signup cohort

CREATE OR REPLACE VIEW analytics.mart_cohort_retention AS
WITH cohort_base AS (
    SELECT
        c.customer_id,
        DATE_TRUNC('month', c.signup_date)::DATE AS cohort_month,
        f.snapshot_month,
        f.is_active,
        (
            EXTRACT(YEAR FROM AGE(f.snapshot_month, DATE_TRUNC('month', c.signup_date)))
            * 12
            + EXTRACT(MONTH FROM AGE(f.snapshot_month, DATE_TRUNC('month', c.signup_date)))
        )::INTEGER AS period_number
    FROM staging.dim_customer c
    INNER JOIN analytics.fact_customer_monthly f
        ON c.customer_id = f.customer_id
),
cohort_size AS (
    SELECT cohort_month, COUNT(DISTINCT customer_id) AS cohort_customers
    FROM cohort_base
    WHERE period_number = 0
    GROUP BY cohort_month
)
SELECT
    b.cohort_month,
    b.period_number,
    cs.cohort_customers,
    COUNT(DISTINCT b.customer_id) FILTER (WHERE b.is_active) AS retained_customers,
    ROUND(
        100.0 * COUNT(DISTINCT b.customer_id) FILTER (WHERE b.is_active)
        / NULLIF(cs.cohort_customers, 0),
        2
    ) AS retention_rate_pct
FROM cohort_base b
INNER JOIN cohort_size cs ON b.cohort_month = cs.cohort_month
GROUP BY b.cohort_month, b.period_number, cs.cohort_customers
ORDER BY b.cohort_month, b.period_number;
