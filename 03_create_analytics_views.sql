CREATE SCHEMA IF NOT EXISTS s3_stock_analytics;

CREATE OR REPLACE VIEW s3_stock_analytics.market_summary_view AS
SELECT
    COUNT(DISTINCT symbol) AS total_stocks,
    ROUND(AVG(daily_return_pct), 2) AS avg_market_return,
    ROUND(AVG(volume), 0) AS avg_volume
FROM s2_stock_clean.stock_prices;


CREATE OR REPLACE VIEW s3_stock_analytics.top_gainers_view AS
SELECT
    symbol,
    date,
    daily_return_pct
FROM s2_stock_clean.stock_prices
ORDER BY daily_return_pct DESC
LIMIT 10;


CREATE OR REPLACE VIEW s3_stock_analytics.top_losers_view AS
SELECT
    symbol,
    date,
    daily_return_pct
FROM s2_stock_clean.stock_prices
ORDER BY daily_return_pct ASC
LIMIT 10;


CREATE OR REPLACE VIEW s3_stock_analytics.stock_comparison_view AS
SELECT
    symbol,
    ROUND(AVG(close), 2) AS avg_close_price,
    ROUND(AVG(daily_return_pct), 2) AS avg_return,
    ROUND(AVG(volume), 0) AS avg_volume
FROM s2_stock_clean.stock_prices
GROUP BY symbol;


CREATE OR REPLACE VIEW s3_stock_analytics.volume_leaders_view AS
SELECT
    symbol,
    AVG(volume) AS avg_volume
FROM s2_stock_clean.stock_prices
GROUP BY symbol
ORDER BY avg_volume DESC;
