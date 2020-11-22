# visualizing various aspects of the data - being backtset information of statistical information

import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from pandas_datareader import data as web
import plotly.graph_objects as go
from datetime import datetime

# plots price at open / close over past week
def plot_open_close(ticker_name, time_period):
    ticker = yf.Ticker(ticker_name)
    df = ticker.history(period = time_period)
    df[['Open','Close']].plot()
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.title(ticker_name)
    plt.show()

# plots highs over past week
def plot_high(ticker_name, time_period):
    ticker = yf.Ticker(ticker_name)
    df = ticker.history(period = time_period)
    print(df[['High']])
    df[['High']].plot()
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.title(ticker_name)
    plt.show()

# plots the daily highs of multiple stocks
def plot_stocks(stocks, time_period):
    frames = []

    for i in stocks:
        ticker_name = i
        ticker = yf.Ticker(i)
        df = ticker.history(period = time_period)
        df = df[['High']]
        df.rename(columns={'High':ticker_name}, inplace=True)
        frames.append(df)
    
    df = pd.concat(frames, axis=1)
    print(df)

    df.plot()
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.title("Stock Prices")
    
    plt.show()

def plot_candle(stocks,start_date):
    
    ticker = yf.Ticker(stocks)
    dfy = ticker.history(period = '1mo')
    #print(df)
    high_data = dfy[['High']]
    open_data = dfy[['Open']]
    low_data = dfy[['Low']]
    close_data = dfy[['Close']]
    #dates = df[['Date']]
    df = df = web.DataReader(stocks, data_source='yahoo', start=start_date)
    trace1 = trace1 = {
    'x': df.index,
    'open': df.Open,
    'close': df.Close,
    'high': df.High,
    'low': df.Low,
    'type': 'candlestick',
    'name': 'MSFT',
    'showlegend': True
}

    fig = go.Figure(data=[trace1])

    fig.show()
    
if __name__ == "__main__":
    #plot_open_close("AAPL", "5d")

    #plot_high("AAPL", "5d")

    #stocks = ["AAPL", "GOOGL", "AMZN", "TSLA"]
    #plot_stocks(stocks, "1mo")
    plot_candle("AAPL",'01-01-2019') #having issues extracting the dates