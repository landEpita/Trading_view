from devise import *
import matplotlib.pyplot as plt

import numpy as np
import datetime
from dateutil.relativedelta import *
from nn import *

def interpolate(name,year,month,day):
    date = datetime.date(year,month,day)

    date_e = date - datetime.timedelta(days=1)
    date_b = date - relativedelta(months=+12)
    #print(date_b, " to ", date_e, " avec " ,date)
    devise = Devise(name, 
            (date_b.year, date_b.month, date_b.day),
            (date_e.year, date_e.month, date_e.day))
    tmp = devise.rbf(devise.date[len(devise.date)-1]+1)
    devise.pt_x.append(devise.date[len(devise.date)-1]+1)
    devise.pt_y.append(tmp)
    x = np.array(devise.pt_x)
    y = np.array(devise.pt_y) + devise.first
    #print(tmp+devise.first)
    #print(x)
    #print(y)

    #plt.plot(x,y)
    #plt.plot(devise.date, devise.y+devise.first)
    #plt.show()
    if y[-1] > y[-2]:
        return True
    return False

def strat_interpolate(devise):
    max_holding = 100
    indexx=devise.data.index
    holdings = pd.DataFrame(index=indexx, data={'Holdings': np.array([np.nan] *
        len(indexx))})
    #print(holdings)
    for i in indexx:
        y = i.year
        m = i.month
        d = i.day
        #print(type(i))
        tmp = interpolate(devise.name, y, m, d)
        if tmp:
            holdings.loc[i, 'Holdings'] = max_holding
        else:
            holdings.loc[i, 'Holdings'] = 0
    print(holdings)
    holdings.ffill(inplace=True)
    holdings.fillna(0, inplace=True)
    #print(holdings)
    holdings['Order'] = holdings.diff()
    holdings.dropna(inplace=True)
    print(holdings)

    return holdings


def print_holding_inter(devise, ax1):

    holdings = strat_interpolate(devise)

    # Plot the buy signals
    ax1.plot(devise.data.loc[holdings.loc[(holdings["Order"] > 0)].index]['Adj Close'], 
             '^', markersize=10, color='green', label="Buy RSI")
             
    # Plot the sell signals
    ax1.plot(devise.data.loc[holdings.loc[(holdings['Order'] < 0)].index]['Adj Close'],
             'v', markersize=10, color='red', label="Sell RSI")
    return ax1


def main():

    #symbols = ["AAPL", "GOOG", "MSFT", "AMZN", "SNY", "NTDOY", "IBM", "HPQ", "QCOM", "NVDA"]
    

    appl = Devise("IBM", (2018,1,1), (2018,12,30))
    setx = appl.set_train()
    #print(setx)
    nn = Genome()
    l = np.array(setx.values.tolist())
    #print(l)
    
    print(nn.run(l[100:101]))

    print(nn.getweith())

         

main()


