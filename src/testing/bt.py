from __future__ import (absolute_import, division, print_function,
                            unicode_literals)


import backtrader as bt
import backtrader.indicators as btind
import datetime
import os.path
import sys
from devise import *


class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=15)
        self.rsi = bt.indicators.RelativeStrengthIndex()

    def notify_order(self, order):
        #print(order.status)
        #print([order.Submitted, order.Accepted], order.Completed)
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
#                self.log(
#                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
#                    (order.executed.price,
#                     order.executed.value,
#                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
#            else:  # Sell
#                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
#                         (order.executed.price,
#                          order.executed.value,
#                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        #self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
         #        (trade.pnl, trade.pnlcomm))

    def next(self):
        #self.log('Close, %.2f' % self.dataclose[0])
        #print('rsi:', self.rsi[0])
        if self.order:
            return

        if not self.position:
            if (self.rsi[0] < 30):
        #        self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy(size=500)

        else:
            if (self.rsi[0] > 70):
         #       self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell(size=500)


if __name__ == '__main__':
    symbols = ["AAPL"]#, "GOOG", "MSFT", "AMZN", "SNY", "NTDOY", "IBM", "HPQ", "QCOM", "NVDA"]

    money = 100000.0

    for s in symbols:
        print(s)
        cerebro = bt.Cerebro()
        cerebro.addstrategy(TestStrategy)
        cerebro.broker.setcommission(commission=0.001)

        data = bt.feeds.YahooFinanceData(
            dataname = s,
            fromdate=datetime.datetime(2017, 1, 1),
            todate=datetime.datetime(2019, 1, 1),
            reverse = False
        )
        cerebro.adddata(data, name=s)

        cerebro.broker.setcash(money)
        print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
        cerebro.run()
        money = cerebro.broker.getvalue()
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
