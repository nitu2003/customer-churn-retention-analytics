-- Customer segment churn: demographics, contract, and service mix

DROP VIEW IF EXISTS vw_segment_churn_demographics;
DROP VIEW IF EXISTS vw_segment_churn_services;
DROP VIEW IF EXISTS vw_segment_churn_unified;

CREATE VIEW vw_segment_churn_demographics AS
SELECT
    b.gender,
    b.senior_citizen_label,
    b.partner,
    b.dependents,
    COUNT(*) AS customer_count,
    SUM(b.is_churned) AS churned_customers,
    ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct,
    ROUND(SUM(b.monthly_charges), 2) AS total_monthly_revenue,
    ROUND(SUM(b.churned_monthly_revenue), 2) AS churned_monthly_revenue
FROM vw_base_customers b
GROUP BY
    b.gender,
    b.senior_citizen_label,
    b.partner,
    b.dependents;

CREATE VIEW vw_segment_churn_services AS
SELECT
    b.internet_service,
    b.phone_service,
    b.contract,
    b.tech_support,
    b.online_security,
    COUNT(*) AS customer_count,
    SUM(b.is_churned) AS churned_customers,
    ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct,
    ROUND(SUM(b.monthly_charges), 2) AS total_monthly_revenue
FROM vw_base_customers b
GROUP BY
    b.internet_service,
    b.phone_service,
    b.contract,
    b.tech_support,
    b.online_security;

-- Long-format segment table for Power BI matrix / slicer combos
CREATE VIEW vw_segment_churn_unified AS
SELECT
    s.segment_type,
    s.segment_value,
    s.customer_count,
    s.churned_customers,
    s.churn_rate_pct,
    s.total_monthly_revenue,
    s.churned_monthly_revenue,
    ROUND(s.churn_rate_pct - p.portfolio_churn_rate_pct, 2) AS lift_vs_portfolio_pct
FROM (
    SELECT 'gender' AS segment_type, b.gender AS segment_value,
           COUNT(*) AS customer_count, SUM(b.is_churned) AS churned_customers,
           ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct,
           ROUND(SUM(b.monthly_charges), 2) AS total_monthly_revenue,
           ROUND(SUM(b.churned_monthly_revenue), 2) AS churned_monthly_revenue
    FROM vw_base_customers b GROUP BY b.gender
    UNION ALL
    SELECT 'senior_citizen', b.senior_citizen_label, COUNT(*), SUM(b.is_churned),
           ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2),
           ROUND(SUM(b.monthly_charges), 2), ROUND(SUM(b.churned_monthly_revenue), 2)
    FROM vw_base_customers b GROUP BY b.senior_citizen_label
    UNION ALL
    SELECT 'partner', b.partner, COUNT(*), SUM(b.is_churned),
           ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2),
           ROUND(SUM(b.monthly_charges), 2), ROUND(SUM(b.churned_monthly_revenue), 2)
    FROM vw_base_customers b GROUP BY b.partner
    UNION ALL
    SELECT 'dependents', b.dependents, COUNT(*), SUM(b.is_churned),
           ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2),
           ROUND(SUM(b.monthly_charges), 2), ROUND(SUM(b.churned_monthly_revenue), 2)
    FROM vw_base_customers b GROUP BY b.dependents
    UNION ALL
    SELECT 'contract', b.contract, COUNT(*), SUM(b.is_churned),
           ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2),
           ROUND(SUM(b.monthly_charges), 2), ROUND(SUM(b.churned_monthly_revenue), 2)
    FROM vw_base_customers b GROUP BY b.contract
    UNION ALL
    SELECT 'internet_service', b.internet_service, COUNT(*), SUM(b.is_churned),
           ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2),
           ROUND(SUM(b.monthly_charges), 2), ROUND(SUM(b.churned_monthly_revenue), 2)
    FROM vw_base_customers b GROUP BY b.internet_service
    UNION ALL
    SELECT 'payment_method', b.payment_method, COUNT(*), SUM(b.is_churned),
           ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2),
           ROUND(SUM(b.monthly_charges), 2), ROUND(SUM(b.churned_monthly_revenue), 2)
    FROM vw_base_customers b GROUP BY b.payment_method
    UNION ALL
    SELECT 'paperless_billing', b.paperless_billing, COUNT(*), SUM(b.is_churned),
           ROUND(100.0 * SUM(b.is_churned) / NULLIF(COUNT(*), 0), 2),
           ROUND(SUM(b.monthly_charges), 2), ROUND(SUM(b.churned_monthly_revenue), 2)
    FROM vw_base_customers b GROUP BY b.paperless_billing
) s
CROSS JOIN (
    SELECT ROUND(100.0 * SUM(is_churned) / NULLIF(COUNT(*), 0), 2) AS portfolio_churn_rate_pct
    FROM vw_base_customers
) p;
