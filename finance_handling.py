# given in statistical info, dataframe as well as user params to make decision on if to invest and how much
import numpy as np
import scipy.stats as stats
from stats_functions import ma

#get moving average across multiple sized previous periods and dictate current distance fromt he mean
def movavg_crossover(short_period,long_period,funds,curr_value):
    #TODO MAKE SURE TO CALL PROPER FUNCTION ONCE IMPLIMENTED
    long_avg = ma(period=long_period)
    short_avg = ma(period=short_period)
    
    buy_flag = long_avg < short_avg
    potential_gains = curr_value - long_avg

    print(long_period+" Average" + str(long_avg))
    print(short_period+" Average" + str(short_avg))
    print("Potential Returns: " + str(potential_gains))
    if(buy_flag):
        print("BUY")
    else:
        print("DONT BUY")
    return