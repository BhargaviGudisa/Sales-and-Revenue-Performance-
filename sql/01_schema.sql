-- ============================================================
-- Schema: sales
-- Source: data/processed/sales_data_clean.csv
-- Description: One row per line-item transaction. Loaded via
--              scripts/build_sqlite_db.py for local analysis;
--              the same DDL applies to any SQL warehouse
--              (Postgres, SQL Server, Snowflake, etc.) with
--              minor type-syntax adjustments.
-- ============================================================

CREATE TABLE IF NOT EXISTS sales (
    order_id          TEXT,
    order_date        DATE,
    ship_date         DATE,
    ship_mode         TEXT,
    customer_id       TEXT,
    customer_name     TEXT,
    segment           TEXT,
    region            TEXT,
    city              TEXT,
    state             TEXT,
    postal_code       TEXT,
    category          TEXT,
    sub_category      TEXT,
    product_id        TEXT,
    product_name      TEXT,
    sales             NUMERIC,
    quantity          INTEGER,
    discount          NUMERIC,
    profit            NUMERIC,
    profit_margin     NUMERIC,
    order_year        INTEGER,
    order_month       INTEGER,
    order_year_month  TEXT
);
