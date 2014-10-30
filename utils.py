import numpy as np
from decimal import *


class Utils(object):

    def __init__(self):
        self.within_percent = lambda x,y,o: ((y*(1-o)) <= x) and (x <= (y*(1+o)))

    def trend(self, prices):
        return [b - a for a, b in zip(prices[::1], prices[1::1])]

    def trend_percent(self, prices):
        return [(b - a)/b for a, b in zip(prices[::1], prices[1::1])]   
    def movingAverage(self,values,window):
        weigths = np.repeat(1.0, window)/window
        smas = np.convolve(values, weigths, 'valid')
        return smas # as a numpy array
    def getRSI(self,prices, n=14):
        n = Decimal(n)
        deltas = np.diff(prices)
        seed = deltas[:n+1.0]
        up = seed[seed>=0.0].sum()/n
        down = -seed[seed<0.0].sum()/n
        rs = up/down
        rsi = np.zeros_like(prices)
        rsi[:n] = 100.0 - 100.0/(1.0+rs)
        for i in range(n,len(prices)):
            delta = deltas[i-1]
            if delta > 0.0:
                upval = delta
                downval = 0.0
            else:
                upval = 0.0
                downval = -delta
            up = (up*(n-1.0)+upval)/n
            down = (down*(n-1.0)+downval)/n
            rs = up/down
            rsi[i] = 100.0 - 100.0/(1.0+rs)
        return rsi

    def detrend(self, prices, ma):
        n = 0
        ret = []
        for p in prices:
            dt = (p-ma[n])/ma[n]
            ret.append(dt)
            n += 1
        return ret

    def getTrend(self, prices):
        
        pmax = np.amax(prices)
        pmin = np.amin(prices)
        if type(prices) != list:
            prices = prices.tolist()
        if prices.index(pmax) > prices.index(pmin):
            return 1
        else:
            return -1
