import yfinance as yf
import datetime
from tqdm import tqdm

from load import load_every_fifteen
from stats_functions import *

class Strategy:
    #maps strings to functions
    str_to_function = {
        'MA' : moving_average,
        'rsi': rsi,
        'mfi': mfi,
        'candle_patterns': candle_stick
    }

    def __init__(self,capital,strategy_list=['MA'],risk='medium',stock_list=None):
        self.cash = capital
        self.strategy_list = self.init_strat_functions(strategy_list)
        self.risk = ['low','medium','high'].index(risk)
        self.history = None
        self.curr_investments = dict()

        if stock_list == None:
            #TODO HAVE WAY TO HAVE PREMADE LIST OF STOCKS TO WATCH
            self.stock_list = ['AAPL', 'MSFT', 'TSLA']

        self.stock_list = stock_list

        self.__gen_investments_dict()

    #populates the strategies current holdings
    def __gen_investments_dict(self):
        #populating the dict with all money in cash
        for i in self.stock_list:
            self.curr_investments[i] = 0
        self.curr_investments['cash'] = self.cash
        return
    
    #returns list of functions to be used on backtester
    def init_strat_functions(self,strats):
        return [Strategy.str_to_function[i] for i in strats]

    
    def backtest_eval(self,start_date,end_date):
        #values to be determined from entire backtest
        total_earnings = 0
        transaction_history = []

        #used for bug testing
        # start_date = datetime.date(2020, 10, 20)
        # end_date = datetime.date(2020, 10, 22)
        start_date = datetime.date(*start_date)
        curr_date = start_date
        end_date = datetime.date(*end_date)
        delta = datetime.timedelta(days=1)

        #change for for loop later for loading bar package
        while start_date <= end_date:
            print("Eval on " + curr_date)
            day_investments = self.evaluate_current_day(self.strategy_list, self.stock_list,self.cash,curr_date)
            
            transaction_history.append(self.buy_sell_stocks(day_investments))
            curr_date += delta
        
        return
    
    def evaluate_current_day(self,strategy_list, stock_list, cash,date):
        daily_investments = []

        for stock in stock_list:
            for strat in strategy_list:
                #expecting info like [buy/sell amount, num_shares,date, stock]
                #TODO ADD RISK FACTOR
                daily_investments.append(strat(date, stock, cash))

        return daily_investments

    #TODO IMPLIMENT THE METHOD OF KEEPING TRACK OF CURRENT SHARE HOLDINGS
    #must also update the transactions list once bought or sold 
    #current niave approach
    def buy_sell_stocks(self,investments):
        transactions = []

        for i in investments:
            #need to check if have proper number of shares to sell TODO
            #checking if have cash to buy security
            if self.curr_investments['cash'] - i[0] >= 0:
                self.curr_investments['cash'] -= i[0]
                transactions.append(i)


x = Strategy(1000)