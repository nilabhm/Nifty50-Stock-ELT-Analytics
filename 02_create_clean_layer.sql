CREATE SCHEMA IF NOT EXISTS s2_stock_clean;

CREATE TABLE IF NOT EXISTS s2_stock_clean.stock_prices AS
SELECT
    date,
    symbol,
    open,
    high,
    low,
    close,
    volume,
    ROUND((close - open)::numeric, 2) AS price_change,
    ROUND(
        (((close - open) / NULLIF(open, 0)) * 100)::numeric,
        2
    ) AS daily_return_pct
FROM s1_stock_raw.stock_prices;
