import pandas_datareader as pdr
import datetime
import pandas as pd
import numpy as np
import math

import matplotlib.pyplot as plt

from scipy.interpolate import Rbf, InterpolatedUnivariateSpline

from math import log, sqrt


from devise import *

def strat_RSI(devise):
    max_holding = 100
    indexx=devise.data.index
    holdings = pd.DataFrame(index=indexx, data={'Holdings': np.array([np.nan] *
        len(indexx))})
    #print(holdings)
    holdings.loc[((devise.op_data['RSI'] < 30) & (devise.op_data['BBP'] < 0)), 'Holdings'] = max_holding
    holdings.loc[((devise.op_data['RSI'] > 70) & (devise.op_data['BBP'] > 1)), 'Holdings'] = 0
    #print(holdings)
    holdings.ffill(inplace=True)
    holdings.fillna(0, inplace=True)
    #print(holdings)
    holdings['Order'] = holdings.diff()
    holdings.dropna(inplace=True)
    #print(holdings)

    return holdings

def strat_MA_CHIKU(devise):

    max_holding = 100
    indexx=devise.data.index
    holdings = pd.DataFrame(index=indexx, data={'Holdings': np.array([np.nan] *
        len(indexx))})
    
    #print(holdings)
    #holdings.loc[((((devise.op_data['RSI'] < 30) & (devise.op_data['BBP'] < 0)) | (devise.op_data['RSI'] > 50)) &
    #    (devise.ichimoku['chikou_span'].shift(26) > devise.data['Close'].shift(26)))
    #        , 'Holdings'] = max_holding

    #holdings.loc[
    #        ((((devise.op_data['RSI'] > 70) & (devise.op_data['BBP'] > 1)) | (devise.op_data['RSI'] < 50)) &
    #            (devise.ichimoku['chikou_span'].shift(26) < devise.data['Close'].shift(26)))
    #        , 'Holdings'] = 0


    #print(holdings)
    holdings.loc[((devise.op_data['RSI'] < 30) & (devise.op_data['BBP'] < 0))
            , 'Holdings'] = max_holding

    holdings.loc[
            ((((devise.op_data['RSI'] > 70) & (devise.op_data['BBP'] > 1)) |
                (devise.ichimoku['chikou_span'].shift(26) < devise.data['Close'].shift(26))))
            , 'Holdings'] = 0


    #print(holdings)
    holdings.ffill(inplace=True)
    holdings.fillna(0, inplace=True)
    #print(holdings)
    holdings['Order'] = holdings.diff()
    holdings.dropna(inplace=True)
    #print(holdings)

    return holdings


def strat_MA(devises, l):
    max_holding = 100

    short_window = 20
    long_window = 100

    short = devises.data['Adj Close'].rolling(window=short_window).mean()
    #if (l==[]):
    #    longs = devises.data['Adj Close'].rolling(window=long_window).mean()
    #else:
    longs = l

    indexx=devises.data.index
    holdings = pd.DataFrame(index=indexx, data={'Holdings': np.array([np.nan] *
        len(indexx))})
    #print(holdings)
    holdings.loc[(short > longs), 'Holdings'] = max_holding
    holdings.loc[(short < longs), 'Holdings'] = 0
    #print(holdings)
    holdings.ffill(inplace=True)
    holdings.fillna(0, inplace=True)
    #print(holdings)
    holdings['Order'] = holdings.diff()
    holdings.dropna(inplace=True)
    #print(holdings)

    return holdings

def strategy_1_ichi(devise):
    max_holding = 100
    indexx=devise.data.index
    holdings = pd.DataFrame(index=indexx, data={'Holdings': np.array([np.nan] *
        len(indexx))})
    #print(holdings)
    holdings.loc[
            ((devise.data['Close']  > devise.ichimoku['senkou_span_a']) & 
                (devise.data['Close']  > devise.ichimoku['senkou_span_b'])&
                (devise.ichimoku['tenkan_sen']  > devise.ichimoku['senkou_span_a'])&
                (devise.ichimoku['tenkan_sen']  > devise.ichimoku['senkou_span_b'])&
                (devise.ichimoku['kijun_sen']  > devise.ichimoku['senkou_span_a'])&
                (devise.ichimoku['kijun_sen']  > devise.ichimoku['senkou_span_b'])&
                (devise.ichimoku['kijun_sen']  < devise.ichimoku['tenkan_sen'])&
                (devise.ichimoku['chikou_span'] > devise.ichimoku['senkou_span_a'].shift(26))&
                (devise.ichimoku['chikou_span'] > devise.ichimoku['senkou_span_b'].shift(26)))
            , 'Holdings']= max_holding


    holdings.loc[ 
            ((devise.data['Close']  < devise.ichimoku['senkou_span_a']) & 
                (devise.data['Close']  < devise.ichimoku['senkou_span_b'])&
                (devise.ichimoku['tenkan_sen']  < devise.ichimoku['senkou_span_a'])&
                (devise.ichimoku['tenkan_sen']  < devise.ichimoku['senkou_span_b'])&
                (devise.ichimoku['kijun_sen']  < devise.ichimoku['senkou_span_a'])&
                (devise.ichimoku['kijun_sen']  < devise.ichimoku['senkou_span_b'])&
                (devise.ichimoku['kijun_sen']  > devise.ichimoku['tenkan_sen'])&
                (devise.ichimoku['chikou_span'] < devise.ichimoku['senkou_span_a'].shift(26))&
                (devise.ichimoku['chikou_span'] < devise.ichimoku['senkou_span_b'].shift(26)))
            , 'Holdings'] = 0
    #print(holdings)
    holdings.ffill(inplace=True)
    holdings.fillna(0, inplace=True)
    #print(holdings)
    holdings['Order'] = holdings.diff()
    holdings.dropna(inplace=True)
    return holdings

def strategy_2_ichi(devise): #Cloud technique
    max_holding = 100
    indexx=devise.data.index
    holdings = pd.DataFrame(index=indexx, data={'Holdings': np.array([np.nan] *
        len(indexx))})
    #print(holdings)
    holdings.loc[
            ((devise.data['Close']  > devise.ichimoku['senkou_span_a']) & 
                (devise.data['Close']  > devise.ichimoku['senkou_span_b']))
            , 'Holdings']= max_holding


    holdings.loc[ 
            ((devise.data['Close']  < devise.ichimoku['senkou_span_a']) & 
                (devise.data['Close']  < devise.ichimoku['senkou_span_b']))
            , 'Holdings'] = 0
    #print(holdings)
    holdings.ffill(inplace=True)
    holdings.fillna(0, inplace=True)
    #print(holdings)
    holdings['Order'] = holdings.diff()
    holdings.dropna(inplace=True)
    #print(holdings)
    return holdings

def strategy_3_ichi(devise): #Cloud technique
    max_holding = 100
    indexx=devise.data.index
    holdings = pd.DataFrame(index=indexx, data={'Holdings': np.array([np.nan] *
        len(indexx))})
    #print(holdings)
    holdings.loc[
            ((devise.ichimoku['senkou_span_a']  > devise.ichimoku['senkou_span_b']) &
                ((devise.data['Close']  > devise.ichimoku['senkou_span_a']) & 
                (devise.data['Close']  > devise.ichimoku['senkou_span_b'])))
            , 'Holdings']= max_holding


    holdings.loc[ 
            ((devise.ichimoku['senkou_span_b'] > devise.ichimoku['senkou_span_a'])|
                ((devise.data['Close']  < devise.ichimoku['senkou_span_a']) & 
                (devise.data['Close']  < devise.ichimoku['senkou_span_b']))) 
            , 'Holdings'] = 0
    #print(holdings)
    holdings.ffill(inplace=True)
    holdings.fillna(0, inplace=True)
    #print(holdings)
    holdings['Order'] = holdings.diff()
    holdings.dropna(inplace=True)
    #print(holdings)
    return holdings


def strategy_4_ichi(devise): #Chikou tecnique
    max_holding = 100
    indexx=devise.data.index
    holdings = pd.DataFrame(index=indexx, data={'Holdings': np.array([np.nan] *
        len(indexx))})
    #print(holdings)
    holdings.loc[
            ((devise.ichimoku['chikou_span'].shift(26) > devise.data['Close'].shift(26)))
            , 'Holdings']= max_holding


    holdings.loc[ 
           ((devise.ichimoku['chikou_span'].shift(26) < devise.data['Close'].shift(26)))
            , 'Holdings'] = 0
    #print(holdings)
    holdings.ffill(inplace=True)
    holdings.fillna(0, inplace=True)
    #print(holdings)
    holdings['Order'] = holdings.diff()
    holdings.dropna(inplace=True)
    #print(holdings)
    return holdings

def resume(devise, somme=(-1)):
    save = somme
    holdings = strategy_1_ichi(devise)
    tab = holdings.loc[((holdings['Order'] > 0) | (holdings['Order'] < 0))]
    n = 0
    a = 0
    total = 0
    nb = 0
    tmp = 0
    txt = ""
    txt += "########Resume########\n"
    for day , h in tab.iterrows():
        if n%2 != 0:
            a += devise.data.loc[day]["Adj Close"]
            total += a
            txt += str(day) + " : Sold at "+ str(devise.data.loc[day]["Adj Close"])+"\n"
            txt += "delta : "+str(a) + "\n"
            if save >=0:
                somme = somme + (nb * devise.data.loc[day]["Adj Close"])
                txt += "Compte : "+str(somme) + "\n"
            nb = 0
            a = 0
        else:
            if save >= 0:
                tmp = somme
                nb = int(somme / devise.data.loc[day]["Adj Close"])
                somme = int(somme % devise.data.loc[day]["Adj Close"])
            txt += str(day) + " : Buy at " + str(devise.data.loc[day]["Adj Close"]) +" nb :"+ str(nb) + "\n"
            a -= devise.data.loc[day]["Adj Close"]
        n+=1
    if a != 0 and save > (-1):
        somme = tmp
    txt += "total = " + str(total) +" somme = "+  str(somme) +"\n"
    return (((somme/save) - 1), somme, txt)

