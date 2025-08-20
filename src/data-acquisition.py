import yfinance as yf
import pandas as pd
import requests
from pytickersymbols import PyTickerSymbols
import os
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')

# BASE_URL = "https://www.alphavantage.co/query"
# ALPHA_KEY = 'W910QMTXDZFKET8Y'

print("Starting data acquisition...")
# Step 1: Fetch S&P 100 symbols
stock_data = PyTickerSymbols()
sp100 = stock_data.get_stocks_by_index('S&P 100')
symbols = [stock['symbol'] for stock in sp100]
print(f"Fetched {len(symbols)} symbols from S&P 100.")

# Step 2: Date range
today = datetime.now()
start_date = (today - timedelta(days=365)).strftime('%Y-%m-%d')
end_date = today.strftime('%Y-%m-%d')

# Step 3: Download all data in batch
print("Fetching 1 year OHLCV data from Yahoo Finance...")
data = yf.download(
    tickers=symbols,
    start=start_date,
    end=end_date,
    group_by='ticker',
    auto_adjust=False
)

# create a csv and parquet file with the data and save it in data/raw
print("Saving data to CSV...")
data = data.stack(level=0).rename_axis(['Date', 'Ticker']).reset_index()
data.to_csv("data/raw/sp100_1y.csv", index=False)      
print("Saving data to Parquet...")
data.to_parquet("data/raw/sp100_1y.parquet", index=False)

# print the head of dataframe
print("Sample data from Yahoo Finance:", data.head())


#use alphavantage to fetch the data, using the API key from the .env file named ALPHAVANTAGE_API_KEY
# api_key = os.getenv('ALPHAVANTAGE_API_KEY')
# ts = TimeSeries(key='W910QMTXDZFKET8Y', output_format='pandas')
# for symbol in symbols:
#     print(f"Fetching data for {symbol} from Alpha Vantage...")
#     data, meta_data = ts.get_daily(symbol=symbol, outputsize='full')
#     print(f"Data for {symbol} from Alpha Vantage fetched successfully.", meta_data)
#     #create a dataframe with the data
#     df_av = pd.DataFrame(data)
#     # Optionally, you can also save the data to a CSV file
#     print(f"Data for {symbol} from Alpha Vantage fetched successfully.")  

# print("Data acquisition completed successfully.")