-- Power BI: pre-aggregated monthly churn KPIs

CREATE OR REPLACE VIEW bi.vw_mart_churn_monthly AS
SELECT * FROM analytics.mart_churn_monthly;
