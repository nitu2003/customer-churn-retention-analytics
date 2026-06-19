-- Customer Churn & Retention Analytics Platform
-- 01_ddl: Schema and base tables
-- Adjust dialect-specific syntax as needed (PostgreSQL shown)

CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS bi;

-- Dimension: customer
CREATE TABLE IF NOT EXISTS staging.dim_customer (
    customer_id       VARCHAR(64) PRIMARY KEY,
    signup_date       DATE NOT NULL,
    region            VARCHAR(64),
    segment           VARCHAR(64),
    acquisition_channel VARCHAR(128),
    created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimension: plan
CREATE TABLE IF NOT EXISTS staging.dim_plan (
    plan_id           VARCHAR(32) PRIMARY KEY,
    plan_name         VARCHAR(128) NOT NULL,
    plan_tier         VARCHAR(32),
    list_price_mrr    NUMERIC(12, 2)
);

-- Fact: subscriptions
CREATE TABLE IF NOT EXISTS staging.fact_subscriptions (
    subscription_id   VARCHAR(64) PRIMARY KEY,
    customer_id       VARCHAR(64) NOT NULL REFERENCES staging.dim_customer(customer_id),
    plan_id           VARCHAR(32) NOT NULL REFERENCES staging.dim_plan(plan_id),
    start_date        DATE NOT NULL,
    end_date          DATE,
    status            VARCHAR(32) NOT NULL,
    mrr               NUMERIC(12, 2)
);

-- Fact: monthly customer snapshot (grain: customer × month)
CREATE TABLE IF NOT EXISTS analytics.fact_customer_monthly (
    customer_id       VARCHAR(64) NOT NULL,
    snapshot_month    DATE NOT NULL,
    is_active         BOOLEAN NOT NULL,
    is_churned        BOOLEAN NOT NULL,
    mrr               NUMERIC(12, 2),
    usage_score       NUMERIC(10, 4),
    tenure_months     INTEGER,
    PRIMARY KEY (customer_id, snapshot_month)
);
