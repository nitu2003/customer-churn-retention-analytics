-- Power BI: row-level customer detail (drill-through / table visuals)

DROP VIEW IF EXISTS vw_pbi_customer_detail;

CREATE VIEW vw_pbi_customer_detail AS
SELECT
    customer_id,
    customer_status,
    is_churned,
    churn_risk_band,
    gender,
    senior_citizen_label,
    partner,
    dependents,
    tenure,
    tenure_bucket,
    tenure_bucket_sort,
    contract,
    internet_service,
    phone_service,
    payment_method,
    paperless_billing,
    tech_support,
    online_security,
    monthly_charges,
    total_charges,
    churned_monthly_revenue,
    at_risk_monthly_revenue
FROM vw_base_customers;
