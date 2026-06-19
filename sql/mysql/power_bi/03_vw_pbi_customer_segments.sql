-- Power BI: customer segment churn views

DROP VIEW IF EXISTS vw_pbi_segment_churn_demographics;
DROP VIEW IF EXISTS vw_pbi_segment_churn_services;
DROP VIEW IF EXISTS vw_pbi_segment_churn_unified;

CREATE VIEW vw_pbi_segment_churn_demographics AS
SELECT * FROM vw_segment_churn_demographics;

CREATE VIEW vw_pbi_segment_churn_services AS
SELECT * FROM vw_segment_churn_services;

CREATE VIEW vw_pbi_segment_churn_unified AS
SELECT * FROM vw_segment_churn_unified;
