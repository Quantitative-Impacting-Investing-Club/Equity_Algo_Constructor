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

    if mfi > 70:
        return pd.DataFrame({'stock':ticker_name,'date':date,'action':"sell"})
    if mfi < 30:
        return pd.DataFrame({'stock':ticker_name,'date':date,'action':"buy"})
    else:
        return None

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
    
    if rsi > 70:
        return pd.DataFrame({'stock':ticker_name,'date':date,'action':"sell"})
    if rsi < 30:
        return pd.DataFrame({'stock':ticker_name,'date':date,'action':"buy"})
    else:
        return None


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


def calculate_ma(ticker_name, interval, date):
    ticker = yf.Ticker(ticker_name)
    
    delta = datetime.timedelta(days=interval+50)
    df = ticker.history(start=date-delta, end=date)
    df = df[['Close']]
    df.reset_index(level=0, inplace=True)
    df.columns=['ds','y']

    df['SMA_20'] = df.y.rolling(window=20).mean()
    df['SMA_50'] = df.y.rolling(window=50).mean()
    df.drop(index=list(range(50)), inplace=True)

    plt.plot(df.ds, df.y, label=ticker_name)
    plt.plot(df.ds, df.SMA_20, label=ticker_name+' 20 Day SMA', color='orange')
    plt.plot(df.ds, df.SMA_50, label=ticker_name+' 50 Day SMA', color='magenta')

    df['EMA_12'] = df.y.ewm(span=12,adjust=False).mean()
    df['EMA_26'] = df.y.ewm(span=26,adjust=False).mean()
    df['MACD'] = df.EMA_12 - df.EMA_26
    df['EMA_9'] = df.MACD.ewm(span=9,adjust=False).mean()

    plt.plot(df.ds, df.MACD, label=ticker_name+' MACD', color = '#EBD2BE')
    plt.plot(df.ds, df.EMA_9, label='Signal Line', color='#E5A4CB')
    plt.legend(loc='upper left')
    plt.show()


def candlestick_strategy(ticker_name, interval,current_date):
    #candle stick can do long intervals since yfinance provides open, close,highs and lows for a long range of dates
    date_list = [current_date - datetime.timedelta(days=x) for x in range(interval)]
    date_list.reverse()
    #from start of interval to end of interval
    actionFlag = False
    sellFlag = False
    buyFlag = False
    transactions = pd.DataFrame(columns=['stock','date','action'])
    for tickers in ticker_name:
        ticker = yf.Ticker(ticker_name)
        delta = datetime.timedelta(days=interval)
        df = ticker.history(start=current_date-delta, end=current_date) 
        dates = df.index
        df.insert(0, "Date", df.index, True)
        df.insert(0, "Index", list(range(len(df.index))), True)
        df.set_index("Index", inplace=True)
        #print(df)
        runningStats = pd.DataFrame(columns=['gainCheck','change','ratio','swing','peakSwingRatio','date'])
        for i in range(len(df.index)):
            normalizedDate = date.strftime("%Y-%m-%d")
            currentOpen = df.loc[i,'Open']
            currentClose = df.loc[i,'Close']
            currentLow = df.loc[i,'Low']
            currentHigh = df.loc[i,'High']
            #print(currentOpen)
            #print(currentClose)
            #print(currentLow)
            #print(currentHigh)
            runningStatsFrame = pd.DataFrame({'gainCheck': (currentOpen > currentClose), 'change':currentOpen-currentClose,
            'ratio':abs((currentOpen-currentClose)/currentOpen),'swing':currentHigh-currentLow,
            'peakSwingRatio': abs((currentOpen-currentClose)/(currentHigh-currentLow)),'date':dates[i]},index = [i])
            runningStats = runningStats.append(runningStatsFrame)
            if(i > 2): #3 day candlestick patterns
                
                #the numbers here are kinda arbitrary ngl, thats why theyre all precomputed, so we can change them
                negativeTrend = df.loc[i-2,'Close'] > currentClose
                positiveTrend = df.loc[i-2,'Close'] < currentClose

                hammerThickness = 0.25
                hammerCheckTop = currentHigh/currentOpen*(0.2) < runningStats['swing'][i]
                hammerCheckMid = runningStats['peakSwingRatio'][i] < hammerThickness

                TBCThreshold = 0.7
                ThreeBlackCrowsCheck = ((runningStats['peakSwingRatio'][i] > TBCThreshold) and (runningStats['peakSwingRatio'][i-1] > TBCThreshold)
                and (runningStats['peakSwingRatio'][i-2]) > TBCThreshold)

                TLSThreshold = 0.4
                ThreeLineStrikeCheck = ((runningStats['peakSwingRatio'][i] > TLSThreshold) and (runningStats['peakSwingRatio'][i-1] > TLSThreshold)
                and (runningStats['peakSwingRatio'][i-2]) > TLSThreshold)


                gapCheck = ((currentOpen-df.loc[i-1,'Close'])/df.loc[i-1,'Close']) > 0.04 #if the stock loses 4% or more overnight
                if(negativeTrend and runningStats['gainCheck'][i] and hammerCheckTop and hammerCheckMid):
                    buyFlag = True
                    actionFlag = True
                    print("Hammer")
                    #hammer
                elif(negativeTrend and ThreeBlackCrowsCheck):
                    buyFlag = True
                    actionFlag = True
                    print("Three black Crows")
                    #three black crows
                elif(positiveTrend and ThreeLineStrikeCheck):
                    sellFlag = True
                    actionFlag = True
                    print("Three line Strike (bear)")
                    #Three Line strike (bear)
                elif(negativeTrend and ThreeLineStrikeCheck):
                    buyFlag = True
                    actionFlag = True
                    print("Three line Strike (bull)")
                    #Three Line strike (bull)
                elif(gapCheck):
                    sellFlag = True
                    actionFlag = True
                    print("Gap")
                    #gap
                #recognize the trends
                if(actionFlag):
                    actionFlag = False
                    if(sellFlag == True):
                        sellFlag = False
                        #sell and add to transactions
                        transFrame = pd.DataFrame({'stock':ticker_name,'date':dates[i],'action':"sell"},[len(transactions)])
                        print("Trans")
                        print(transFrame)
                        transactions = transactions.append(transFrame)
                        #data.update({'c':3,'d':4})  # Updates 'c' and adds 'd'
                    elif(buyFlag == True):
                        buyFlag = False
                        #buy and add to transactions
                        transFrame = pd.DataFrame({'stock':ticker_name,'date':dates[i],'action':"buy"}, index = [len(transactions)])
                        print("Trans")
                        print(transFrame)
                        transactions = transactions.append(transFrame)

    #print(runningStats)
    #print(df)
    print(transactions)
    return transactions
    #expecting returned info like [buy/sell amount, num_shares,date, stock]


if __name__ == "__main__":
    date = datetime.datetime.today()

    #print("RSI: " + str(calculate_rsi("AAPL", date)))
    
    #plot_rsi("AAPL", 30, date)

    #print("MFI: " + str(calculate_mfi("AAPL", date)))
    
    #plot_mfi("AAPL", 30, date)
    
    #candlestick_strategy('AAPL',25,date)

    plot_macd("AAPL", 365, date)