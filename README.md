# Nifty 50 Stock ETL & Analytics Pipeline

An end-to-end stock-market data project that extracts recent Nifty 50 stock data, transforms it through layered PostgreSQL schemas, creates analytical SQL views, and connects the analytics layer to Power BI for dashboarding.

## Project Architecture

```text
Yahoo Finance
     |
     v
Python + yFinance
     |
     v
Pandas Transformation
     |
     v
PostgreSQL - Raw Layer
s1_stock_raw.stock_prices
     |
     v
PostgreSQL - Clean Layer
s2_stock_clean.stock_prices
     |
     v
PostgreSQL - Analytics Layer
s3_stock_analytics
     |
     v
Analytical Views
     |
     v
Power BI
     |
     v
Interactive Dashboard
```

A visual version of this flow is available at `docs/project_flow.png`.

## What the Project Does

1. Downloads approximately one month of price data for a list of Nifty 50 stocks using yFinance.
2. Handles the MultiIndex structure that can be returned by yFinance.
3. Standardizes column names and prepares the raw dataset.
4. Loads the extracted data into PostgreSQL.
5. Creates a clean layer with:
   - Price change
   - Daily return percentage
6. Creates an analytics layer with SQL views for:
   - Market summary
   - Top gainers
   - Top losers
   - Stock comparison
   - Volume leaders
7. Connects the PostgreSQL analytics layer to Power BI to build the final dashboard.

## Technology Stack

- Python
- Pandas
- yFinance
- PostgreSQL
- SQLAlchemy
- SQL
- Power BI

## Database Architecture

### 1. Raw Layer — `s1_stock_raw`

Stores the extracted stock-price data:

- `date`
- `open`
- `high`
- `low`
- `close`
- `volume`
- `symbol`

### 2. Clean Layer — `s2_stock_clean`

Adds derived metrics:

- `price_change`
- `daily_return_pct`

### 3. Analytics Layer — `s3_stock_analytics`

Contains five analytical views:

- `market_summary_view`
- `top_gainers_view`
- `top_losers_view`
- `stock_comparison_view`
- `volume_leaders_view`

## Repository Structure

```text
Nifty50-Stock-ETL-Analytics/
|
|-- python/
|   `-- stock_etl.py
|
|-- sql/
|   |-- 01_create_raw_layer.sql
|   |-- 02_create_clean_layer.sql
|   `-- 03_create_analytics_views.sql
|
|-- dashboard/
|   `-- README.md
|
|-- media/
|   `-- README.md
|
|-- docs/
|   `-- project_flow.png
|
|-- .env.example
|-- .gitignore
|-- requirements.txt
`-- README.md
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Nifty50-Stock-ETL-Analytics.git
cd Nifty50-Stock-ETL-Analytics
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure PostgreSQL credentials

Copy `.env.example` to `.env` and enter your local PostgreSQL credentials.

**Never commit `.env` to GitHub.**

### 4. Create the database layers

Run the SQL scripts in this order:

```text
01_create_raw_layer.sql
02_create_clean_layer.sql
03_create_analytics_views.sql
```

### 5. Run the ETL script

```bash
python python/stock_etl.py
```

The script downloads the data and loads it into:

```text
s1_stock_raw.stock_prices
```

### 6. Connect Power BI

Connect Power BI to PostgreSQL and use the analytics views in:

```text
s3_stock_analytics
```

The final dashboard is intended to present market-level and stock-level insights from the transformed data.

## Project Walkthrough Video

A project walkthrough video will be added to:

```text
media/project_walkthrough.mp4
```

The video should demonstrate:

1. Python ETL script
2. PostgreSQL raw layer
3. Clean layer
4. Analytics views
5. Power BI connection
6. Final dashboard
7. Key insights

## Notes

- The project uses local PostgreSQL, so another user will need PostgreSQL configured locally to reproduce the pipeline.
- The Python script uses environment variables for database credentials so secrets are not stored in source code.
- The stock list and data period can be changed directly in `python/stock_etl.py`.
- The project is for data engineering/analytics learning and portfolio demonstration, not investment advice.
