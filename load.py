import yfinance as yf
import matplotlib.pyplot as plt

def get_stock(ticker):
    #get ticker object
    ticker = yf.Ticker(ticker)
    #information about ticker
    print(ticker.info)
    print(ticker.actions)
    #get time series data
    df = ticker.history()
    print(df)
    print(df.describe())
    print(df.columns)
    print(df.index)
    #indexing columns
    print(df['Open'])
    print(df[['Open','Close']])

    print(df['Open'][0])
    print(df[['Open','Close']].iloc[0])
    print(df[['Open','Close']].loc['2020-09-10'])
    #indexing rows this data
    print(df.loc['2020-09-10'])
    print(df.iloc[0])

    print(df.loc['2020-09-10':'2020-09-20'])
    print(df.iloc[0:5])

    return(df[['Open','Close']])


def plot_findat(df):
    df.plot()
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()
    
if __name__ == "__main__":
    df = get_stock("AAPL")
    plot_findat(df)