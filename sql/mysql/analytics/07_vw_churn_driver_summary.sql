-- Churn driver summary: churn rate and lift vs portfolio for each categorical driver

DROP VIEW IF EXISTS vw_churn_driver_summary;

CREATE VIEW vw_churn_driver_summary AS
SELECT
    d.driver_category,
    d.driver_value,
    d.customer_count,
    d.churned_customers,
    d.churn_rate_pct,
    p.portfolio_churn_rate_pct,
    ROUND(d.churn_rate_pct - p.portfolio_churn_rate_pct, 2) AS lift_vs_portfolio_pct,
    ROUND(
        d.churn_rate_pct / NULLIF(p.portfolio_churn_rate_pct, 0),
        2
    ) AS churn_index,
    d.total_monthly_revenue,
    d.churned_monthly_revenue,
    RANK() OVER (
        PARTITION BY d.driver_category
        ORDER BY d.churn_rate_pct DESC
    ) AS churn_rank_in_category
FROM (
    SELECT 'contract' AS driver_category, b.contract AS driver_value,
           COUNT(*) AS customer_count, SUM(b.is_churned) AS churned_customers,
           ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct,
           ROUND(SUM(b.monthly_charges), 2) AS total_monthly_revenue,
           ROUND(SUM(b.churned_monthly_revenue), 2) AS churned_monthly_revenue
    FROM vw_base_customers b GROUP BY b.contract

    UNION ALL SELECT 'internet_service', b.internet_service, COUNT(*), SUM(b.is_churned),
           ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2),
           ROUND(SUM(b.monthly_charges), 2), ROUND(SUM(b.churned_monthly_revenue), 2)
    FROM vw_base_customers b GROUP BY b.internet_service

    UNION ALL SELECT 'payment_method', b.payment_method, COUNT(*), SUM(b.is_churned),
           ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2),
           ROUND(SUM(b.monthly_charges), 2), ROUND(SUM(b.churned_monthly_revenue), 2)
    FROM vw_base_customers b GROUP BY b.payment_method

    UNION ALL SELECT 'phone_service', b.phone_service, COUNT(*), SUM(b.is_churned),
           ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2),
           ROUND(SUM(b.monthly_charges), 2), ROUND(SUM(b.churned_monthly_revenue), 2)
    FROM vw_base_customers b GROUP BY b.phone_service

    UNION ALL SELECT 'tech_support', b.tech_support, COUNT(*), SUM(b.is_churned),
           ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2),
           ROUND(SUM(b.monthly_charges), 2), ROUND(SUM(b.churned_monthly_revenue), 2)
    FROM vw_base_customers b GROUP BY b.tech_support

    UNION ALL SELECT 'online_security', b.online_security, COUNT(*), SUM(b.is_churned),
           ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2),
           ROUND(SUM(b.monthly_charges), 2), ROUND(SUM(b.churned_monthly_revenue), 2)
    FROM vw_base_customers b GROUP BY b.online_security

    UNION ALL SELECT 'paperless_billing', b.paperless_billing, COUNT(*), SUM(b.is_churned),
           ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2),
           ROUND(SUM(b.monthly_charges), 2), ROUND(SUM(b.churned_monthly_revenue), 2)
    FROM vw_base_customers b GROUP BY b.paperless_billing

    UNION ALL SELECT 'partner', b.partner, COUNT(*), SUM(b.is_churned),
           ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2),
           ROUND(SUM(b.monthly_charges), 2), ROUND(SUM(b.churned_monthly_revenue), 2)
    FROM vw_base_customers b GROUP BY b.partner

    UNION ALL SELECT 'dependents', b.dependents, COUNT(*), SUM(b.is_churned),
           ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2),
           ROUND(SUM(b.monthly_charges), 2), ROUND(SUM(b.churned_monthly_revenue), 2)
    FROM vw_base_customers b GROUP BY b.dependents

    UNION ALL SELECT 'senior_citizen', b.senior_citizen_label, COUNT(*), SUM(b.is_churned),
           ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2),
           ROUND(SUM(b.monthly_charges), 2), ROUND(SUM(b.churned_monthly_revenue), 2)
    FROM vw_base_customers b GROUP BY b.senior_citizen_label

    UNION ALL SELECT 'gender', b.gender, COUNT(*), SUM(b.is_churned),
           ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2),
           ROUND(SUM(b.monthly_charges), 2), ROUND(SUM(b.churned_monthly_revenue), 2)
    FROM vw_base_customers b GROUP BY b.gender

    UNION ALL SELECT 'tenure_bucket', b.tenure_bucket, COUNT(*), SUM(b.is_churned),
           ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2),
           ROUND(SUM(b.monthly_charges), 2), ROUND(SUM(b.churned_monthly_revenue), 2)
    FROM vw_base_customers b GROUP BY b.tenure_bucket
) d
CROSS JOIN (
    SELECT ROUND(100.0 * SUM(is_churned) / NULLIF(COUNT(*), 0), 2) AS portfolio_churn_rate_pct
    FROM vw_base_customers
) p;
