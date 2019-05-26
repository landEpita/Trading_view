import pandas_datareader as pdr
import datetime
import pandas as pd
import numpy as np
import math

import matplotlib.pyplot as plt

from scipy.interpolate import Rbf, InterpolatedUnivariateSpline

from math import log, sqrt


from devise import *
from strat import *

def pourcentage_annee():
    current_date = datetime.date(2019,1,1)
    begin_date = datetime.date(2016,1,1)
    symbols = ["AAPL", "GOOG", "MSFT", "AMZN", "SNY", "NTDOY", "IBM", "HPQ", "QCOM", "NVDA"]
    while begin_date != current_date:
        pc = []
        somme_total = 0
        d = begin_date.replace(year=begin_date.year + 1)
        for s in symbols:
            print(s)
            appl = Devise(s, (begin_date.year,begin_date.month,begin_date.day), (d.year,d.month,d.day))
            pp , somme, _ = resume(appl, 100000)
            somme_total += somme
            pc.append(pp)
        plt.barh(symbols, pc, align='center',
            color='green', ecolor='black')
        print(somme_total)
        plt.show()
        begin_date = begin_date.replace(year=begin_date.year + 1)

def pourcentage_duree():
    pc = [] 
    current_date = datetime.date(2019,1,1)
    begin_date = datetime.date(2016,1,1)
    symbols = ["AAPL", "GOOG", "MSFT", "AMZN", "SNY", "NTDOY", "IBM", "HPQ", "QCOM", "NVDA"]
    somme_total = 0
    for s in symbols:
        print(s)
        appl = Devise(s, (begin_date.year,begin_date.month,begin_date.day), (current_date.year,current_date.month,current_date.day))
        pp , somme, _ = resume(appl, 100000)
        somme_total += somme
        pc.append(pp)
    plt.barh(symbols, pc, align='center',
        color='green', ecolor='black')
    print(somme_total)
    plt.show()


def print_holding_RSI(devise, ax1):

    holdings = strat_RSI(devise)

    # Plot the buy signals
    ax1.plot(devise.data.loc[holdings.loc[(holdings["Order"] > 0)].index]['Adj Close'], 
             '^', markersize=10, color='green', label="Buy RSI")
             
    # Plot the sell signals
    ax1.plot(devise.data.loc[holdings.loc[(holdings['Order'] < 0)].index]['Adj Close'],
             'v', markersize=10, color='red', label="Sell RSI")

def print_holding_MA(devise, ax1, hold):

    holdings = strat_MA(devise, hold)

    # Plot the buy signals
    ax1.plot(devise.data.loc[holdings.loc[(holdings["Order"] > 0)].index]['Adj Close'], 
             '^', markersize=10, color='#3af2f9', label="Buy MA")
             
    # Plot the sell signals
    ax1.plot(devise.data.loc[holdings.loc[(holdings['Order'] < 0)].index]['Adj Close'],
             'v', markersize=10, color='#f93ad2', label="Sell MA")

def print_holding_MA_CHIKU(devise, ax1):

    holdings = strat_MA_CHIKU(devise)

    # Plot the buy signals
    ax1.plot(devise.data.loc[holdings.loc[(holdings["Order"] > 0)].index]['Adj Close'], 
             '^', markersize=10, color='#3af2f9', label="Buy MA")
             
    # Plot the sell signals
    ax1.plot(devise.data.loc[holdings.loc[(holdings['Order'] < 0)].index]['Adj Close'],
             'v', markersize=10, color='#f93ad2', label="Sell MA")

def print_holding_ICHI(devise, ax1, n):

    if n == 1:
        holdings = strategy_1_ichi(devise)
    elif n == 2:
        holdings = strategy_4_ichi(devise)
    else :
        holdings = strategy_3_ichi(devise)


    # Plot the buy signals
    ax1.plot(devise.data.loc[holdings.loc[(holdings["Order"] > 0)].index]['Adj Close'], 
             '^', markersize=10, color='#3af2f9', label="Buy ichi")
             
    # Plot the sell signals
    ax1.plot(devise.data.loc[holdings.loc[(holdings['Order'] < 0)].index]['Adj Close'],
             'v', markersize=10, color='#f93ad2', label="Sell ichi")

def print_BB(devise, ax2):
    index = devise.op_data.index
    ax2.plot(index, devise.op_data['BB_up'], label='BB_up')
    ax2.plot(index, devise.op_data['BB_low'], label='BB_low')
    ax2.fill_between(index, y1=devise.op_data['BB_low'], y2=devise.op_data['BB_up'], color='#adccff', alpha='0.3')



def print_holding(devise, holdings, ax1):


    # Plot the buy signals
    ax1.plot(devise.data.loc[holdings.loc[(holdings["Order"] > 0)].index]['Adj Close'], 
             '^', markersize=10, color='#3af2f9', label="Buy")
             
    # Plot the sell signals
    ax1.plot(devise.data.loc[holdings.loc[(holdings['Order'] < 0)].index]['Adj Close'],
             'v', markersize=10, color='#f93ad2', label="Sell")

