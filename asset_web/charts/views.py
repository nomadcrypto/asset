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

    period = "%sx %s" % (str(len(chartdata) -1), steps[step])

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


def chart(request, chart_type, market, pair, step):
    chart_types = {"detrend": detrend}
    asset, display_periods = setup_asset(request, market, pair, step)
    chartdata, asset_data = chart_types[chart_type](asset)
    response = build_response(request, asset, chartdata, asset_data, step, display_periods)
    return HttpResponse(simplejson.dumps(response), content_type='application/json')




def chart_old(request, market, pair, step):
    steps = {"1min":60, "5min":300, "15min":900, "30min":1800, "1hr":3600, "1d":86400}

    asset = Asset(market,pair)
    prices = asset.getTicks(steps[step])
    asset.setup(prices)

    display_periods = request.GET.get('display_periods')

    #the moving average starts at 12 so our first 12 prices wont have a movingaverage
    total_prices = len(asset.priceInfo.prices)
    ma_total = len(asset.priceInfo.stats.ma)
    dma_total = len(asset.priceInfo.stats.dma)
    total_offset = total_prices - dma_total
    ma_offset = ma_total-dma_total

    n = 0
    ma = [["Date", "Price High", "Price Low", "12 MA", "Detrend 12ma", "Detrend 12ma OP"],]
    ret = []
    base = 1.000
    start_amount = base
    quote = 0.00
    last_buy = False
    last_buy_sell = False
    start = 0
    if display_periods != None:
        start = ma_total - int(display_periods)

    asset_data = {"market":market, "pair": pair}

    for price in asset.priceInfo.prices[total_offset:]:
        man = n + ma_offset
        dma = asset.priceInfo.stats.ma[man] * (1+asset.priceInfo.stats.dma[n])
        dma_op = asset.priceInfo.stats.ma[man] * (1+asset.priceInfo.stats.dma_op[n])
        time_close = price[4].strftime("%b %d %H:%M")
        res = [time_close,price[3],price[2],asset.priceInfo.stats.ma[man], dma, dma_op]
        ret.append(res)
        n += 1


    if display_periods != None:
        display_periods = int(display_periods)
        ma.extend(ret[len(ret)-display_periods:])
        priceInfo = asset.getPriceInfo(asset.priceInfo.prices[total_prices-display_periods:])
    else:
        priceInfo = asset.priceInfo
        ma.extend(ret)

    period = "%sx %s" % (str(len(ma) -1), step)

    asset_data = {"market":market, "pair": pair, "period": period, 
        "volatility": np.round(priceInfo.volatility*100,2),
        "average_lhp_diff": np.round(priceInfo.average_lhp_diff*100,2),
        }

    response = {"ma":ma, "asset_data": asset_data}
    #return render(request, "chart.html", response)
    return HttpResponse(simplejson.dumps(response), content_type='application/json')

def charts(request):
    return render(request, "chart.html")


    


