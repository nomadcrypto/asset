import json
import time
import simplejson
import numpy as np

from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers


from asset.asset import Asset

steps = {"1min":60, "5min":300, "15min":900, "30min":1800, "1hr":3600, "1d":86400}

def setup_asset(request, market, pair, step):
    

    asset = Asset(market,pair)
    prices = asset.getTicks(steps[step])
    asset.setup(prices)

    display_periods = request.GET.get('display_periods')

    return asset, display_periods


def build_response(request, asset, chartdata, asset_data, step, display_periods):
    if display_periods != None:
        display_periods = int(display_periods)
        chartdata.extend(asset_data[len(asset_data)-display_periods:])
        total_prices = len(asset.priceInfo.prices)
        priceInfo = asset.getPriceInfo(asset.priceInfo.prices[total_prices-display_periods:])
    else:
        priceInfo = asset.priceInfo
        chartdata.extend(asset_data)

    period = "%sx %s" % (str(len(chartdata) - 1), step)
    asset_display_data = {"market":asset.market, "pair": asset.pair, "period": period, 
        "volatility": np.round(priceInfo.volatility*100,2),
        "average_lhp_diff": np.round(priceInfo.average_lhp_diff*100,2),
        }

    return {"chartdata":chartdata, "asset_display_data": asset_display_data}

def detrend(asset):
    total_prices = len(asset.priceInfo.prices)
    ma_total = len(asset.priceInfo.stats.ma)
    dma_total = len(asset.priceInfo.stats.dma)
    total_offset = total_prices - dma_total
    ma_offset = ma_total-dma_total

    n = 0
    chartdata = [["Date", "Price High", "Price Low", "12 MA", "Detrend 12ma", "Detrend 12ma OP"],]
    asset_data = []

    for price in asset.priceInfo.prices[total_offset:]:
        man = n + ma_offset
        dma = asset.priceInfo.stats.ma[man] * (1+asset.priceInfo.stats.dma[n])
        dma_op = asset.priceInfo.stats.ma[man] * (1+asset.priceInfo.stats.dma_op[n])
        time_close = price[4].strftime("%b %d %H:%M")
        res = [time_close,price[3],price[2],asset.priceInfo.stats.ma[man], dma, dma_op]
        asset_data.append(res)
        n += 1
    return chartdata, asset_data

def candlestick(asset):

    chartdata = [["Date", "Price Low", "Price Open", "Price Close", "Price High"],]
    asset_data = []

    for price in asset.priceInfo.prices:
        time_close = price[4].strftime("%b %d %H:%M")
        res = [time_close,price[2],price[0],price[1], price[3]]
        asset_data.append(res)
    return chartdata, asset_data

def rsi(asset):

    chartdata = [["Date", "RSI"],]
    asset_data = []
    prices = [p[1] for p in asset.priceInfo.prices]
    rsis = asset.strat.getRSI(prices)
    n= 0
    for price in asset.priceInfo.prices:
        time_close = price[4].strftime("%b %d %H:%M")
        res = [time_close,rsis[n]]

        asset_data.append(res)
        n +=1 
    return chartdata, asset_data




def chart(request, chart_type, market, pair, step):
    chart_types = {"detrend": detrend, "candlestick": candlestick, "rsi":rsi}
    asset, display_periods = setup_asset(request, market, pair, step)
    chartdata, asset_data = chart_types[chart_type](asset)
    response = build_response(request, asset, chartdata, asset_data, step, display_periods)
    return HttpResponse(simplejson.dumps(response), content_type='application/json')



def charts(request):
    return render(request, "chart.html")


    


