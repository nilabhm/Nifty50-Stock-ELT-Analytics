CREATE SCHEMA IF NOT EXISTS s1_stock_raw;

CREATE TABLE IF NOT EXISTS s1_stock_raw.stock_prices (
    date DATE,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume BIGINT,
    symbol VARCHAR(50)
);
