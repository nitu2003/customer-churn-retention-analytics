-- Power BI: churn driver summary (ranked lifts vs portfolio)

DROP VIEW IF EXISTS vw_pbi_churn_driver_summary;
DROP VIEW IF EXISTS vw_pbi_churn_drivers_top;

CREATE VIEW vw_pbi_churn_driver_summary AS
SELECT * FROM vw_churn_driver_summary;

-- Top drivers per category (churn rank <= 3) for executive visuals
CREATE VIEW vw_pbi_churn_drivers_top AS
SELECT *
FROM vw_churn_driver_summary
WHERE churn_rank_in_category <= 3
  AND customer_count >= 50
ORDER BY driver_category, churn_rank_in_category;
