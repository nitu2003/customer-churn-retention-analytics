-- Optional: create database before first Python load
-- Run in MySQL Workbench or: mysql -u root -p < sql/mysql/01_create_database.sql

CREATE DATABASE IF NOT EXISTS customer_churn_retention_analytics
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE customer_churn_retention_analytics;

-- Tables are created automatically by python/etl/04_load_to_mysql.py via pandas.to_sql.
-- Expected tables after ETL:
--   dim_customers, fact_subscriptions
