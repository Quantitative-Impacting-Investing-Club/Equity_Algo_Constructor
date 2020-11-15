# area for methods for getting statistical values from input data

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# calculates money flow index
def calculate_mfi(ticker_name, date):
    ticker = yf.Ticker(ticker_name)
    
    delta = datetime.timedelta(days=20
                               )
    df = ticker.history(start=date-delta, end=date)

    df = df.tail(15)
    
    # making the index numbers from 0-13 instead of Dates
    df.insert(0, "Date", df.index, True)
    df.insert(0, "Index", list(range(15)), True)
    df.set_index("Index", inplace=True)
    
    print(df)

    positive_mf = 0
    negative_mf = 0
    
    
    # yesterdays typical price
    yesterdays_tp = (df.loc[0, 'High'] + df.loc[0, 'Low'] + df.loc[0, 'Close']) / 3
    for i in range(1, 15):
        todays_tp = (df.loc[i, 'High'] + df.loc[i, 'Low'] + df.loc[i, 'Close']) / 3
        print(todays_tp)
        if todays_tp > yesterdays_tp:
            positive_mf += todays_tp * df.loc[i, 'Volume']
        elif todays_tp < yesterdays_tp:
            negative_mf += todays_tp * df.loc[i, 'Volume']
        yesterdays_tp = todays_tp
    
    money_ratio = positive_mf / negative_mf

    mfi = 100 - (100 / (1 + money_ratio))
    
    print()
    
    return mfi   
 
    
if __name__ == "__main__":
    date = datetime.date(2020, 11, 15)
    print(calculate_mfi("AAPL", date))
    
