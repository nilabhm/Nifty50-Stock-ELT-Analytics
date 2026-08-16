"""
Nifty 50 Stock ETL Pipeline
---------------------------
Extracts 1 month of stock-price data from Yahoo Finance,
transforms it with Pandas, and loads it into PostgreSQL.

Required environment variables:
    DB_USER
    DB_PASS
    DB_HOST (default: localhost)
    DB_PORT (default: 5432)
    DB_NAME (default: postgres)
"""

import os

import pandas as pd
import yfinance as yf
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")

if not DB_USER or not DB_PASS:
    raise ValueError(
        "DB_USER and DB_PASS are required. "
        "Create a local .env file using .env.example."
    )

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

stocks = [
    "ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS",
    "ASIANPAINT.NS", "AXISBANK.NS", "BAJAJ-AUTO.NS",
    "BAJFINANCE.NS", "BAJAJFINSV.NS", "BEL.NS",
    "BHARTIARTL.NS", "CIPLA.NS", "COALINDIA.NS",
    "DRREDDY.NS", "EICHERMOT.NS", "ETERNAL.NS",
    "GRASIM.NS", "HCLTECH.NS", "HDFCBANK.NS",
    "HDFCLIFE.NS", "HEROMOTOCO.NS", "HINDALCO.NS",
    "HINDUNILVR.NS", "ICICIBANK.NS", "INDUSINDBK.NS",
    "INFY.NS", "ITC.NS", "JIOFIN.NS",
    "JSWSTEEL.NS", "KOTAKBANK.NS", "LT.NS",
    "M&M.NS", "MARUTI.NS", "NESTLEIND.NS",
    "NTPC.NS", "ONGC.NS", "POWERGRID.NS",
    "RELIANCE.NS", "SBILIFE.NS", "SBIN.NS",
    "SHRIRAMFIN.NS", "SUNPHARMA.NS",
    "TATACONSUM.NS", "TATASTEEL.NS", "TCS.NS",
    "TECHM.NS", "TITAN.NS", "TRENT.NS",
    "ULTRACEMCO.NS", "WIPRO.NS"
]

all_data = []

for stock in stocks:
    print(f"Downloading {stock}...")

    df = yf.download(
        stock,
        period="1mo",
        progress=False,
        auto_adjust=True
    )

    if df.empty:
        print(f"No data returned for {stock}; skipping.")
        continue

    # Handle MultiIndex returned by yfinance
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Move Date from index to column
    df = df.reset_index()

    # Convert column names to lowercase
    df.columns = [str(col).lower() for col in df.columns]

    # Add stock symbol
    df["symbol"] = stock

    # Keep required columns
    df = df[
        ["date", "open", "high", "low", "close", "volume", "symbol"]
    ]

    all_data.append(df)

if not all_data:
    raise RuntimeError("No stock data was downloaded.")

# Combine all stocks
final_df = pd.concat(all_data, ignore_index=True)

print(final_df.head())
print(f"Final dataset shape: {final_df.shape}")

# Load into PostgreSQL
final_df.to_sql(
    "stock_prices",
    engine,
    schema="s1_stock_raw",
    if_exists="append",
    index=False
)

print("Loaded Successfully")
