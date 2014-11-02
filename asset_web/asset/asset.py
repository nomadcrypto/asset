#system imports
import sys
import time
import json
import requests
import datetime
import numpy as np

#django imports


#application imports
from utils import Utils



class Asset(object):
    
    def __init__(self, market, pair):
        self.market = market
        self.pair = pair
        self.quote,self.base = self.pair.split("_")
        self.strat = Utils()
        self.priceInfo = PriceInfo(self)

    def setup(self, prices):
        self.priceInfo.set_prices(prices)
        self.priceInfo.update()

    def getPriceInfo(self, prices=False):
        if prices == False:
            return self.priceInfo
        else:
            priceInfo = PriceInfo(self)
            priceInfo.set_prices(prices)
            priceInfo.update()
        return priceInfo

    def updatePriceInfo(self, prices=False, priceInfo=False):
        if priceInfo == False:
            self.priceInfo.update(prices)
        else:
            priceInfo = self.getPriceInfo(prices)
            return priceInfo
        return
    
    def tick(self, price):
        self.priceInfo.tick(price)

    def getTicks(self,step="60"):
        
        market = self.market
        if self.market.find("-"):
            market = ''.join(market.split("-"))
        bcwise_name = "%s%s%s" % (market, self.quote, self.base)


        nonce = str(time.time()).split('.')[0]


        url = "https://s5.bitcoinwisdom.com/period?step=%s&sid=6dbb2e46&symbol=%s&nonce=%s" % (step, bcwise_name, nonce)

        r = requests.get(url)
        res = r.json()

        ticks = []
        for tick in res:
            time_close = datetime.datetime.fromtimestamp(float(tick[0]))
            price_open = float(tick[3])
            price_close = float(tick[4])
            price_high = float(tick[5])
            price_low = float(tick[6])
            volume = float(tick[7])
            ticks.append([price_open, price_close, price_low, price_high, time_close, volume])

        return ticks

    def run(self, step):
        prices = self.getTicks(step)
        self.setup(prices)

        #the moving average starts at 12 so our first 12 prices wont have a movingaverage
        total_prices = len(self.priceInfo.prices)
        ma_total = len(self.priceInfo.stats.ma)
        offset = total_prices - ma_total

        n = 0
        response = []
        for price in self.priceInfo.prices[offset:]:
            p = price
            #convert the datetimeobject back to a unix timestamp. 
            #I only did this because the requested output was json
            p[4] = time.mktime(p[4].timetuple())
            #add the 12 period moving average to the tick
            #here you could add all sorts of useful stuff
            #I highly recommend you checkout the detrend and dma/dma_op
            p.append(self.priceInfo.stats.ma[n])
            response.append(p)
            n +=1

        print json.dumps(response)



class PriceInfo(object):
    """docstring for AssetPriceInfo"""
    def __init__(self, asset):
        super(PriceInfo, self).__init__()
        self.asset = asset
        self.prices = False
        self.stats = StatInfo(self)

    def tick(self, tick):
        self.prices.append(tick)
        self.update()

    def set_prices(self, prices):
        self.prices = prices


    def update(self, prices=False):
        
        #hackish but fixes our problems for right meow
        if prices == False:
            prices = self.prices
        
        self.price_opens = [p[0] for p in prices]
        self.price_closes = [p[1] for p in prices]
        self.price_lows = [p[2] for p in prices]
        self.price_highs = [p[3] for p in prices]
        self.changes = [(p[0]/p[1])-1 for p in prices]
        self.avg_change = np.average(self.changes)
        self.variance = [(x - self.avg_change)**2 for x in self.changes]
        self.volatility = np.sqrt(np.average(self.variance))
        self.average_prices = [np.average(p[:4]) for p in prices]
        
        self.average_volume = np.average([p[5] for p in prices])
        self.average_low_price = np.average(self.price_lows)
        self.average_high_price = np.average(self.price_highs)
        #average difference in percent between the high and low
        self.average_lhp_diff = (self.average_high_price-self.average_low_price)/self.average_low_price

        self.average_open_price = np.average(self.price_opens)
        self.average_close_price = np.average(self.price_closes)
        #average difference in percent between the average open and close
        self.average_ocp_diff = (self.average_close_price-self.average_open_price)/self.average_open_price
        ###

        if len(prices) >= 144:
            self.stats.update()




class StatInfo(object):
    """docstring for AssetStatInfo"""
    def __init__(self, priceInfo):
        super(StatInfo, self).__init__()
        self.priceInfo = priceInfo
        self.asset = priceInfo.asset

    def update(self):
        ###
        self.ma = self.asset.strat.movingAverage(self.priceInfo.price_closes,12)
        offset = len(self.priceInfo.price_closes) - len(self.ma)
        self.detrend = np.array(self.asset.strat.detrend(self.priceInfo.price_closes[offset:], self.ma))
        self.dma = self.asset.strat.movingAverage(self.detrend,12)
        self.dma_op = [(d*-1) for d in self.dma]
        self.detrend_mean = np.mean(self.detrend)
        self.detrend_highs = filter(lambda x: x > 0, self.detrend)
        self.detrend_lows = list(set(self.detrend) - set(self.detrend_highs))
        self.detrend_average_high = np.average(self.detrend_highs)
        self.detrend_average_low = np.average(self.detrend_lows)
        ####


if __name__ == "__main__":
    market = sys.argv[1]
    pair = sys.argv[2]
    step = sys.argv[3]
    steps = {"1min":60, "5min":300, "15min":900, "30min":1800, "1hr":3600}
    if step not in steps.keys():
        print "the step must be one of: ", steps.keys()
        sys.exit()
    asset = Asset(market,pair)
    asset.run(steps[step])

