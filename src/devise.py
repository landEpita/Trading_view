import pandas_datareader as pdr
import datetime
import pandas as pd
import numpy as np
import math

import matplotlib.pyplot as plt
from scipy.interpolate import Rbf, InterpolatedUnivariateSpline

from math import log, sqrt

import fix_yahoo_finance as yf
from matplotlib.widgets import Cursor

class Devise:
    #name = ""
    #data = pd.Series()oandapy
    #date = []
    #y = []
    #ius = np.poly1d([0]), period="mtd"
    #rbf = np.poly1d([0])

    #pt_y =[]
    #pt_x =[]
    def __init__(self, name, d0, d1):
        """d = tuple(year,month,day)"""
        self.name = name

        # Récupere les données de la devise sur Yahoo
        self.data = pdr.get_data_yahoo(name,
                          start=datetime.datetime(d0[0], d0[1], d0[2]), 
                          end=datetime.datetime(d1[0], d1[1], d1[2]))
        # Récupere les données de la devise sur Yahoo par minutes

        # Récupere la colone Adj Close et date; return un tuple de list
        str_d0 = str(d0[0])+"-"+str(d0[1])+"-"+str(d0[2])
        str_d1 = str(d1[0])+"-"+str(d1[1])+"-"+str(d1[2])
    
        self.op_data = self.init_Data()
        date, y = self.set_data(self.op_data, "30 Day MA",str_d0, str_d1)
        
        '''   
     # Uniform la list de date sous forme de list de int
        self.date = self.date_uniform(date)
        self.y = y - y[0]
        
        self.pt_x = []
        self.pt_y = []
        for i in range(0,len(self.y),int(len(self.y)/10)):
            self.pt_x.append(self.date[i])
            self.pt_y.append(self.y[i])
        self.ius = InterpolatedUnivariateSpline(self.pt_x, self.pt_y)
        self.rbf = Rbf(self.pt_x, self.pt_y)

        self.p = []
        for i in range(len(self.date)):
            self.p.append(self.ius(self.date[i]))
        '''
        self.ichimoku = self.Ichimoku()


    def set_data(self, devise, data ,d0, d1):
        """
        d = string(2019-03-21) 
        data = "Adj Close"
        """
        l = devise[data].loc[pd.Timestamp(d0):pd.Timestamp(d1)]
        dates =[]
        y = []
        for x in range(len(l)):
            newdate = str(l.index[x])
            newdate = newdate[0:10]
            if math.isnan(l[x]) == False:
                dates.append(newdate)
                y.append(l[x])

        return (dates, y)
        

    def date_uniform(self, date):
        x = []
        for i in range(len(date)):
            tmp = (datetime.datetime.strptime(date[i], "%Y-%m-%d")
                    - datetime.datetime.strptime(date[0], "%Y-%m-%d"))
            x.append(tmp.days)
        return x


    def init_Data(self):


        # courbe Moving Average -> permet de lisser la courbe (c est une moyen)
        indexx = self.data.index
        newdata = pd.DataFrame(index=indexx)


        newdata['30 Day MA'] = self.MA(20)
        # courbe de l'ecart type
        newdata['30 Day STD'] = self.EcartType(20)
        newdata['100 Day MA'] = self.MA(100)

        newdata['BB_up'] = newdata['30 Day MA'] + (newdata['30 Day STD'] * 2)
        newdata['BB_low'] = newdata['30 Day MA'] - (newdata['30 Day STD'] * 2)
        newdata['BBP'] = (self.data['Adj Close'] - newdata['BB_low'] / newdata['BB_up'] - newdata['BB_low'])
        newdata['RSI'] = self.RSI(18)

        return newdata


    def MA(self, n):
        return self.data['Adj Close'].rolling(window=n).mean()

    def EcartType(self, n):
        return self.data['Adj Close'].rolling(window=n).std()

    

    def pprint(self):
        #plt.figure(1)
        ax1 = plt.subplot(211)
        self.data[['Adj Close']].plot(grid=True, ax=ax1)


        ax2= plt.subplot(212)
        self.volatility().plot(grid=True, ax=ax2)
        #plt.show()
        #ax2.plot(self.pt_x, self.pt_y, 'ro')
        #ax2.plot(self.date, self.y)
        #ax2.plot(self.date,self.p)

        plt.show()

    
    def volatility(self, n=14):
        daily_pct_change = self.daily_pourcentage_change()
        vol = daily_pct_change.rolling(n).std() * np.sqrt(n)
        return vol

    def daily_pourcentage_change(self):
        # Assign `Adj Close` to `daily_close`
        daily_close = self.data[['Adj Close']]
        
        # Daily returns
        daily_pct_change = daily_close.pct_change()
        
        # Replace NA values with 0
        daily_pct_change.fillna(0, inplace=True)

        # Inspect daily returns
        #print(daily_pct_change) # pourcentage de difference entre t et t+1

        # Daily log returns, askip c est mieu
        daily_log_returns = np.log(daily_close.pct_change()+1)

        # Print daily log returns
        #print(daily_log_returns)
        return daily_pct_change
    
    def mensuel_pourcentage_change(self):
        # Resample `aapl` to business months, take last observation as value 
        monthly = self.data.resample('BM').apply(lambda x: x[-1])

        # Calculate the monthly percentage change
        return monthly["Adj Close"].pct_change()

    def trimestre_pourcentage_change(self):
        # Resample `aapl` to quarters, take the mean as value per quarter
        quarter = self.data.resample("4M").mean()

        # Calculate the quarterly percentage change
        return quarter["Adj Close"].pct_change()

    def print_change(self):
        # Plot the distribution of `daily_pct_c`
        d = self.daily_pourcentage_change()
        d.hist(bins=50)

        # Show the plot
        plt.show()

        d.plot()
        plt.show()

        # Pull up summary statistics
        print(d.describe())

    def cumulative_daily_rate(self):
        cumu = (1 + self.daily_pourcentage_change()).cumprod()
        #si on le veut par mois
        #cum_monthly_return = cumu.resample("M").mean()
        cumu.plot(figsize=(12,8))
        plt.show()
        return cumu
    
    def RSI(self, n=14):

        # Get just the close
        close = self.data['Adj Close']
        # Get the difference in self.data from previous step
        delta = close.diff()
        # Get rid of the first row, which is NaN since it did not have a previous 
        # row to calculate the differences
        delta = delta[1:] 

        # Make the positive gains (up) and negative gains (down) Series
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0

        # Calculate the SMA
        roll_up2 = up.rolling(n).mean()
        roll_down2 = down.rolling(n).mean().abs()

        # Calculate the RSI based on SMA
        RS2 = roll_up2 / roll_down2
        rsi = 100.0 - (100.0 / (1.0 + RS2))
        return rsi

    def print_BB(self, ax2):
        index = self.op_data.index
        ax2.plot(index, self.op_data['BB_up'], label='BB_up')
        ax2.plot(index, self.op_data['BB_low'], label='BB_low')
        ax2.fill_between(index, y1=self.op_data['BB_low'], y2=self.op_data['BB_up'], color='#adccff', alpha='0.3')


                 
    def Ichimoku(self):
        """
        kumo(nuage):
            Composer de SS1 et SSB agis comme support ou resistance
            projection de 26 dans le future

            En général, les marchés sont haussiers quand Senkou Span A est au-dessus Senkou Span B et vice-versa pour les marchés baissiers.
            Les traders regardent souvent les changements de Kumo, lorsque Senkou Span A et B échangent leurs positions, 
            comme un signal d'un potentiel renversement de tendance.
            
            Il sera préférable de ne chercher que des signaux de vente si le prix est sous le nuage, 
            et d'ignorer les signaux d'achat. A l'inverse, ne cherchez que des signaux d'achat si le prix est au-dessus le nuage, 
            et ignorez les signaux de vente.





            1) Dernier support du marché
            2) Cassure = changement de tendance
            3) Prix dans le nuage = indécision

            SSA > SSB -> haussiere
            SSB > SSA -> baissiere

        Senkou Span A (SSA):
            - moyen entre la tenkan et la kijun
            [Role]
             - represente l'equilibre des prix entre court terme (Tenkan) et moyen terme (Kijun)
             - informe des supports de resistances futurs
             - represente la volatilité des prix

        Senkou Span B (SSB):
            - point moyen entre le plus haut et le plus bas sur 52 derniere periode
            [Role]
             - Support et resistances importants
             - Droite la plus forte
             - Confime le changement de tendance

        Kijun :
            * point moyen du plus haut et du plus bas sur 26 derniere pediode
            * Si le prix est plus haut que la courbe bleue, il pourrait continuer 
              à grimper plus haut. Si le prix est en-dessous la courbe bleue, il pourrait continuer à baisser.

            [Role]
             - Support/Resistance majeurs
             - equilibre du marché: Avertissement porbable retournement de la tendance

        Tenkan :
            point moyen du plus faut et du plus bas des 9 derniere periode -> (max + min)/2
            [Role]
             - Alerte sur la santé du mouvement
             - Volatilité des prix + puissance du mouvement (inclinaison)

        Chikou Span (memoir du passer):
            - cloture des prix retarder de 26 periode
            [Role]
             - indique les potentiel future mouvant de prix
             - Si Chikou Span traverse le prix du bas vers le haut, c'est un signal d'achat. S'il le traverse du haut vers le bas, c'est un signal de vente. 
        """
        high_prices = self.data['High']
        close_prices = self.data['Close']
        low_prices = self.data['Low']
        dates = self.data.index
        #nine_period_high = pd.rolling_max(self.data['High'], window= 9 )
        #nine_period_low = pd.rolling_min(self.data['Low'], window= 9 )

        nine_period_high = self.data['High'].rolling(window=9).max()
        nine_period_low = self.data['Low'].rolling(window=9).min()

        ichi = pd.DataFrame(index=dates)
        ichi['tenkan_sen'] = (nine_period_high + nine_period_low) /2

        # Kijun-sen (Base Line): (26-period high + 26-period low)/2))
        period26_high = high_prices.rolling(window=26).max()
        period26_low = low_prices.rolling(window=26).min()
        ichi['kijun_sen'] = (period26_high + period26_low) / 2

        # Senkou Span A (Leading Span A): (Conversion Line + Base Line)/2))
        ichi['senkou_span_a'] = ((ichi['tenkan_sen'] + ichi['kijun_sen']) / 2).shift(26)

        # Senkou Span B (Leading Span B): (52-period high + 52-period low)/2))
        period52_high = high_prices.rolling(window=52).max()
        period52_low = low_prices.rolling(window=52).min()
        ichi['senkou_span_b'] = ((period52_high + period52_low) / 2).shift(26)

        # The most current closing price plotted 22 time periods behind (optional)
        ichi['chikou_span'] = close_prices.shift(-26) # 22 according to investopedia
        #ichi.plot()
        #close_prices.plot(label="courbe")
        #plt.show()
        return ichi


    def set_train(self):
        indexx=self.data.index
        set_t = pd.DataFrame(index=indexx)

        set_t["Close"] = self.data["Close"] #- self.data.iloc[0]["Close"]
        set_t["RSI"] = self.op_data["RSI"]
        set_t['30 Day MA'] = self.op_data['30 Day MA']
        set_t['tenkan_sen'] = self.ichimoku['tenkan_sen']
        set_t['kijun_sen'] = self.ichimoku['kijun_sen']
        set_t['senkou_span_a'] = self.ichimoku['senkou_span_a']
        set_t['senkou_span_b'] = self.ichimoku['senkou_span_b']
        set_t['chikou_span'] = self.ichimoku['chikou_span']

        set_t['30 Day STD'] = self.op_data['30 Day STD']
        set_t['100 Day MA'] = self.op_data['100 Day MA']

        set_t['BB_up'] = self.op_data['BB_up']
        set_t['BB_low'] = self.op_data['BB_low']
        set_t['BBP'] = self.op_data['BBP']
        return set_t

