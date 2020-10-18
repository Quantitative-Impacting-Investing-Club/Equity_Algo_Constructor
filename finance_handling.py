# given in statistical info, dataframe as well as user params to make decision on if to invest and how much
import numpy as np
import scipy.stats as stats
#from stats_functions import ma

#get moving average across multiple sized previous periods and dictate current distance fromt he mean
def movavg_decs(period,funds,curr_value):
    num_periods = 5
    len_perioid = period[0:1]
    historical_ma = list()

    for i in range(num_periods):
        itter_period = str(len_perioid + len_perioid*i)+period[1:]
        #historical_ma.append(ma(period=itter_period))
    
    potential_gains = curr_value - itter_period[0]
    z_scores = stats.zscore(historical_ma)
    std = np.std(historical_ma)

    print("Potential Returns: " + str(potential_gains))
    print("Z-Score probability of happening: " + str(z_scores[0]))
    return