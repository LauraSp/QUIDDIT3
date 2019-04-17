import numpy as np
import scipy.optimize as op
import sys
from QUtility import *


#def aggregate(T1, NT, T2, IaB_measured, t1, t2):
#    """calculates sqaured difference between measured aggregation and model.
#    """
#    EaR = 81160
#    preexp = 293608
#    NA0 = NT    #A centres before aggregation starts
#    rate1 = preexp * np.exp(-EaR/(T1+273))
#    NA1 =  NA0/(1+(rate1*NA0)*t1)     #A centres after first stage of annealing
#    rate2 = preexp * np.exp(-EaR/(T2+273))
#    NA2 = NA1/(1+(rate2*NA1)*t2)      #A centres after second stage of annealing
#    IaB_calc = 1-(NA2/NT)
#    error = IaB_measured - IaB_calc
#    return error**2

def model(total_duration, core_NT, core_agg, rim_NT, rim_agg):
    """Main model using measured aggregation state to calculate potential T-histories
    """

    stage1 = np.arange(0, total_duration+10, 10)   #possible durations of stage 1 in 10 Ma steps
    stage1[0] = 1
    stage1[-1] = total_duration - 1

    st1 = []
    st2 = []


    for duration in stage1:
        rim_duration = (total_duration - duration) * 1e6 * 365.25 * 24 * 60 * 60
        core_duration = duration * 1e6 * 365.25 * 24 * 60 * 60
        rim_T = QUtility.Temp_N(rim_duration, rim_NT, rim_agg)
        st2.append(rim_T)
        print("rim T: {}".format(rim_T))
        
        res = op.minimize_scalar(QUtility.aggregate, bounds=(700,1500), args=(core_NT, rim_T, core_agg, core_duration, rim_duration), method='bounded')

        print(res)
        core_T = res.x
        st1.append(core_T)

    return stage1, st1, st2

if __name__ == "__main__":
    model(sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
