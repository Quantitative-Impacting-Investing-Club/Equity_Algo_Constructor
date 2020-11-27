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
    df = ticker.history(start=start_date)
    #print(df)
    dates = df.index
    openData = df.loc[:,'Open']
    closeData = df.loc[:,'Close']
    lowData = df.loc[:,'Low']
    highData = df.loc[:,'High']
    dates = df.index
    print(openData)
    fig = go.Figure(data=[go.Candlestick(x=dates,
                       open=openData, high=highData,
                       low=lowData, close=closeData)])
    fig.show()
    
if __name__ == "__main__":
    plot_open_close("AAPL", "5d")

    plot_high("AAPL", "5d")

    stocks = ["AAPL", "GOOGL", "AMZN", "TSLA"]
    plot_stocks(stocks, "1mo")
    plot_candle("AAPL",'2020-01-01') #having issues extracting the dates