-- Power BI: customer dimension view

CREATE OR REPLACE VIEW bi.vw_dim_customer AS
SELECT
    customer_id,
    signup_date,
    region,
    segment,
    acquisition_channel,
    DATE_TRUNC('month', signup_date)::DATE AS signup_cohort_month
FROM staging.dim_customer;
