-- Power BI: revenue at risk views

DROP VIEW IF EXISTS vw_pbi_revenue_at_risk_summary;
DROP VIEW IF EXISTS vw_pbi_revenue_at_risk_by_band;
DROP VIEW IF EXISTS vw_pbi_revenue_at_risk_customers;

CREATE VIEW vw_pbi_revenue_at_risk_summary AS
SELECT * FROM vw_revenue_at_risk_summary;

CREATE VIEW vw_pbi_revenue_at_risk_by_band AS
SELECT * FROM vw_revenue_at_risk_by_band;

CREATE VIEW vw_pbi_revenue_at_risk_customers AS
SELECT * FROM vw_revenue_at_risk_customers;
