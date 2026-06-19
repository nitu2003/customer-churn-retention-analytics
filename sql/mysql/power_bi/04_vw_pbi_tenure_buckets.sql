-- Power BI: tenure bucket views

DROP VIEW IF EXISTS vw_pbi_tenure_bucket_summary;
DROP VIEW IF EXISTS vw_pbi_tenure_bucket_detail;

CREATE VIEW vw_pbi_tenure_bucket_summary AS
SELECT * FROM vw_tenure_bucket_summary;

CREATE VIEW vw_pbi_tenure_bucket_detail AS
SELECT * FROM vw_tenure_bucket_churn_detail;
