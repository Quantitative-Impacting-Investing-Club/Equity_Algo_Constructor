# area for methods for getting statistical values from input data

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# calculates money flow index
def calculate_mfi(ticker_name, date):
    ticker = yf.Ticker(ticker_name)
    
    delta = datetime.timedelta(days=25)
    df = ticker.history(start=date-delta, end=date)

    df = df.tail(15)
    
    # making the index numbers from 0-14 instead of Dates
    df.insert(0, "Date", df.index, True)
    df.insert(0, "Index", list(range(15)), True)
    df.set_index("Index", inplace=True)


    positive_mf = 0
    negative_mf = 0
    
    
    # yesterdays typical price
    yesterdays_tp = (df.loc[0, 'High'] + df.loc[0, 'Low'] + df.loc[0, 'Close']) / 3
    for i in range(1, 15):
        todays_tp = (df.loc[i, 'High'] + df.loc[i, 'Low'] + df.loc[i, 'Close']) / 3
        if todays_tp > yesterdays_tp:
            positive_mf += todays_tp * df.loc[i, 'Volume']
        elif todays_tp < yesterdays_tp:
            negative_mf += todays_tp * df.loc[i, 'Volume']
        yesterdays_tp = todays_tp
    
    money_ratio = positive_mf / negative_mf

    mfi = 100 - (100 / (1 + money_ratio))

    
    return mfi

def calculate_rsi(ticker_name, date):
    ticker = yf.Ticker(ticker_name)
    
    delta = datetime.timedelta(days=25)
    df = ticker.history(start=date-delta, end=date)
    
    df = df.tail(15)
 
    # making the index numbers from 0-14 instead of Dates
    df.insert(0, "Date", df.index, True)
    df.insert(0, "Index", list(range(15)), True)
    df.set_index("Index", inplace=True)


    average_gain = 0
    average_loss = 0
    
    # yesterdays close price
    yesterdays_close = df.loc[0, 'Close']
    for i in range(1, 15):
        todays_close = df.loc[i, 'Close']
        # checks if todays close is greater or less than yesterdays close
        if todays_close > yesterdays_close:
            average_gain += todays_close - yesterdays_close
        else:
            average_loss += yesterdays_close - todays_close
        yesterdays_close = todays_close
    
    # finds average loss and average gain
    average_loss /= 14
    average_gain /= 14

    # calculates rsi
    rsi = 100 - (100 / (1 + average_gain / average_loss))
    
    return rsi


# plots MFI of a stock over given interval
def plot_mfi(ticker_name, interval, current_date):   
    
    # generates list of dates in desired interval
    date_list = [current_date - datetime.timedelta(days=x) for x in range(interval)]
    date_list.reverse()
    
    mfi = [0] * interval
    
    # calculate MFI for each day in desired interval
    for i in range(interval):
        mfi[i] = calculate_mfi(ticker_name, date_list[i])
        
    # makes more readable x-axis values for plot
    dates =[x.strftime("%m-%d-%Y") for x in date_list]
    
    # plot the results
    plt.plot(dates, mfi)
    plt.xlabel('Date')
    plt.ylabel('Money Flow Index')
    plt.title(str("Money Flow Index of " + ticker_name + " over " + str(interval) + " days"))
    plt.show()
    
# plots RSI of a stock over given interval
def plot_rsi(ticker_name, interval, current_date):   
    
    # generates list of dates in desired interval
    date_list = [current_date - datetime.timedelta(days=x) for x in range(interval)]
    date_list.reverse()
    
    rsi = [0] * interval
    
    # calculate RSI for each day in desired interval
    for i in range(interval):
        rsi[i] = calculate_rsi(ticker_name, date_list[i])
        
    # makes more readable x-axis values for plot
    dates =[x.strftime("%m-%d-%Y") for x in date_list]
    
    # plot the results
    plt.plot(dates, rsi)
    plt.xlabel('Date')
    plt.ylabel('Relative Strength Index')
    plt.title(str("Relative Strength Index of " + ticker_name + " over " + str(interval) + " days"))
    plt.show()


if __name__ == "__main__":
    date = datetime.datetime.today()

    print("RSI: " + str(calculate_rsi("AAPL", date)))
    
    plot_rsi("AAPL", 30, date)

    print("MFI: " + str(calculate_mfi("AAPL", date)))
    
    plot_mfi("AAPL", 30, date)
    
