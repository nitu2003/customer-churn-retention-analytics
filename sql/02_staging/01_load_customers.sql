-- Load cleaned customer data into staging
-- Source: data/cleaned/customers.parquet (load via ETL tool or COPY)

TRUNCATE TABLE staging.dim_customer;

-- Example: INSERT from temp table populated by Python/SQL loader
-- INSERT INTO staging.dim_customer (customer_id, signup_date, region, segment, acquisition_channel)
-- SELECT customer_id, signup_date, region, segment, acquisition_channel
-- FROM staging.tmp_customers;
