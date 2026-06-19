-- Enriched customer base (single source for downstream analytics views)
-- Source table: dim_customers (IBM Telco)

DROP VIEW IF EXISTS vw_base_customers;

CREATE VIEW vw_base_customers AS
SELECT
    c.customer_id,
    c.gender,
    c.seniorcitizen AS senior_citizen,
    CASE WHEN c.seniorcitizen = 1 THEN 'Senior' ELSE 'Non-senior' END AS senior_citizen_label,
    c.partner,
    c.dependents,
    c.tenure,
    CASE
        WHEN c.tenure BETWEEN 0 AND 11  THEN '0-11 months'
        WHEN c.tenure BETWEEN 12 AND 23 THEN '12-23 months'
        WHEN c.tenure BETWEEN 24 AND 47 THEN '24-47 months'
        WHEN c.tenure BETWEEN 48 AND 60 THEN '48-60 months'
        WHEN c.tenure >= 61             THEN '61+ months'
        ELSE 'Unknown'
    END AS tenure_bucket,
    CASE
        WHEN c.tenure BETWEEN 0 AND 11  THEN 1
        WHEN c.tenure BETWEEN 12 AND 23 THEN 2
        WHEN c.tenure BETWEEN 24 AND 47 THEN 3
        WHEN c.tenure BETWEEN 48 AND 60 THEN 4
        WHEN c.tenure >= 61             THEN 5
        ELSE 0
    END AS tenure_bucket_sort,
    c.phoneservice AS phone_service,
    c.multiplelines AS multiple_lines,
    c.internetservice AS internet_service,
    c.onlinesecurity AS online_security,
    c.onlinebackup AS online_backup,
    c.deviceprotection AS device_protection,
    c.techsupport AS tech_support,
    c.streamingtv AS streaming_tv,
    c.streamingmovies AS streaming_movies,
    c.contract,
    c.paperlessbilling AS paperless_billing,
    c.paymentmethod AS payment_method,
    CAST(c.monthlycharges AS DECIMAL(12, 2)) AS monthly_charges,
    CAST(c.totalcharges AS DECIMAL(12, 2)) AS total_charges,
    c.churn_label,
    CAST(c.is_churned AS UNSIGNED) AS is_churned,
    CASE WHEN c.is_churned = 1 THEN 'Churned' ELSE 'Active' END AS customer_status,
    CASE
        WHEN c.contract = 'Month-to-month' AND c.tenure < 12 THEN 'High'
        WHEN c.contract = 'Month-to-month' THEN 'Medium'
        WHEN c.internetservice = 'Fiber optic' AND c.is_churned = 0 THEN 'Medium'
        ELSE 'Low'
    END AS churn_risk_band,
    CASE WHEN c.is_churned = 1 THEN CAST(c.monthlycharges AS DECIMAL(12, 2)) ELSE 0 END AS churned_monthly_revenue,
    CASE WHEN c.is_churned = 0 THEN CAST(c.monthlycharges AS DECIMAL(12, 2)) ELSE 0 END AS retained_monthly_revenue,
    CASE
        WHEN c.is_churned = 0 AND c.contract = 'Month-to-month'
        THEN CAST(c.monthlycharges AS DECIMAL(12, 2))
        ELSE 0
    END AS at_risk_monthly_revenue
FROM dim_customers c;
