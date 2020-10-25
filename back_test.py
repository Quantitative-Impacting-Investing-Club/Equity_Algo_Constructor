import yfinance as yf
import datetime
from load import load_every_fifteen

# Responsbile for taking information from stats in as well as user parameters to determine cash made
#from load import get_stock


def algorithmTester(algorithm, stock):
    # timeFrame is a tuple with the start date and end date as strings
    # timeFrame currently is just January 1st 2010 to January 1st 2020
    totalEarnings = 0
    #testStock = get_stock(stock)
    # current the
    # runs the algorithm for every day in a loop between the time frames
    # for day in timeFrame
    start_date = datetime.date(2020, 10, 20)
    startStr = start_date
    end_date = datetime.date(2020, 10, 22)
    delta = datetime.timedelta(days=1)

    while start_date <= end_date:
        totalEarnings += algorithm(start_date, start_date+delta)
        start_date += delta
    print("performance over time period",
          startStr, end_date, "is ", totalEarnings)
    return totalEarnings


def dummyAlgorithm(open, close):
    # buy early sell late
    history = load_every_fifteen(ticker='AAPL', startDate=open, endDate=close)
    buy = history['Open'][0]
    print("buy is ", buy)
    sell = history['Close'][0]
    print("sell is ", sell)
    difference = sell - buy
    return difference


def main():
    performance = algorithmTester(dummyAlgorithm, 'AAPL')
    return performance


main()
