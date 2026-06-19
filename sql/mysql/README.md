# MySQL analytics SQL layer

Analytics views for the IBM Telco churn dataset loaded into `dim_customers`.

## Deploy

```bash
python python/etl/04_load_to_mysql.py
python python/scripts/deploy_mysql_views.py
```

## Layer structure

| Folder | Purpose |
|--------|---------|
| `analytics/` | Business logic views (reusable) |
| `power_bi/` | `vw_pbi_*` views for Power BI Import / DirectQuery |

## Power BI — tables to import

| View | Dashboard use |
|------|----------------|
| `vw_pbi_churn_kpi_summary` | KPI cards |
| `vw_pbi_churn_kpi_dimensions` | Churn by contract / internet / payment |
| `vw_pbi_revenue_at_risk_summary` | Revenue at risk headline |
| `vw_pbi_revenue_at_risk_by_band` | Risk band breakdown |
| `vw_pbi_revenue_at_risk_customers` | Drill-through customer list |
| `vw_pbi_segment_churn_unified` | Segment matrix / bar charts |
| `vw_pbi_tenure_bucket_summary` | Tenure vs churn |
| `vw_pbi_tenure_bucket_detail` | Tenure × contract heatmap |
| `vw_pbi_churn_driver_summary` | Driver ranking with lift |
| `vw_pbi_churn_drivers_top` | Top 3 drivers per category |
| `vw_pbi_customer_detail` | Row-level drill-through |

## Suggested DAX (when using DirectQuery)

```dax
Churn Rate % = AVERAGE(vw_pbi_churn_kpi_summary[churn_rate_pct])
Total Customers = SUM(vw_pbi_churn_kpi_summary[total_customers])
At Risk Revenue = SUM(vw_pbi_revenue_at_risk_summary[prospective_at_risk_revenue])
```

No `.pbix` files are stored in this repository.
