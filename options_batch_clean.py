# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 07:51:42 2016

@author: Dudz
"""

from pandas.io.data import Options
import pandas.io.data as web
import pandas as pd
import datetime
import numpy as np

###############################################################################
#   Calculate the Cummulative Distribution Function for the historical
#   variablity that occurs over the course of time that equals the difference
#   between now and the expiry date of interest
###############################################################################

def cdf(symbol, expiry, price):
    today = datetime.datetime.today()
    today = datetime.date(today.year, today.month, today.day)
    expiry = opt.expiry_dates[1]    
    timedelta = expiry - today    
    
    f = web.DataReader(symbol, 'yahoo')
    f['delta'] = (f['Close'].shift(-timedelta.days) - f['Close']) / f['Close']    
    
    mu = f.delta.mean()
    sigma = f.delta.std()
    
    deltas = np.random.normal(mu, sigma, 5000)
    deltas_sorted = np.sort(deltas)
    prices = (deltas_sorted * price) + price
    
    p = 1. * np.arange(len(deltas)) / (len(deltas) - 1)
    
    return prices, p
    
    

###############################################################################
#   Filter the options results based on desired probably of price being above
#   or below the current price
###############################################################################

def filter_options(sentiment, prices, p, options, prob):
    
    if sentiment == 'bear':
        index = np.where(p > (1 - prob))[0][0]
        price = prices[index]
        
        return options[options.be > price]
        
    elif sentiment == 'bull':
    
        index = np.where(p > prob)[0][0]
        price = prices[index]
        
        return options[options.be < price]
    

###############################################################################
#                           BULL CALL SPREAD
#   Calculate relavent statistics for all of the possible configurations of
#   short and long call positions and return only those that meet certain 
#   criteria ------ SEE BELOW FOR DETAILS
###############################################################################

def bull_call_spread():
    max_profit = []
    break_even = []
    min_loss = []
    short_call = []
    long_call = []
    delta = []
    commission = []
    volume = []
    
    
    strikes = []
    for i in call.index.values:
        if i[0] > (0.9 * price) and i[0] < (1.1 * price):
            strikes.append(i[0])
        
    
    for sc in strikes:
        for lc in strikes:
            if lc <= sc:
                continue
            else:
                sv = call.loc[(sc, slice(None), 'call'), 'Vol'].values[0]
                lv = call.loc[(lc, slice(None), 'call'), 'Vol'].values[0]
                
                vol = np.floor(min([sv, lv]) / 10) * 10
                
                if vol < 5:
                    continue
                
                else:            
                    sp = (call.loc[(sc, slice(None), 'call'), 'Bid'].values[0] + call.loc[(sc, slice(None), 'call'), 'Ask'].values[0]) / 2
                    lp = (call.loc[(lc, slice(None), 'call'), 'Ask'].values[0] + call.loc[(lc, slice(None), 'call'), 'Bid'].values[0]) / 2
                    
                    diff = sp - lp
                    
                    c = (12.95 + (1.25 * vol) * 2)
                    
                    mp = ((lc - sc - (sp - lp)) * 100 * vol) - c
                    be = lc + (sp - lp)
                    ml = -(((sp - lp)) * 100 * vol) + c
                    
                    if mp < 0:
                        continue
                    
                    else:
                        max_profit.append(mp)
                        break_even.append(be)
                        min_loss.append(ml)
                        short_call.append(sc)
                        long_call.append(lc)
                        delta.append(diff)
                        volume.append(vol)
                        commission.append(c)
                    
                    
    df = pd.DataFrame({'symbol': ([s] * len(max_profit))})
    df['expiry'] = expiry
    df['sentiment'] = 'bull'
    df['underlying_price'] = price
    df['sc'] = short_call
    df['lc'] = long_call
    df['delta'] = delta
    df['mp'] = max_profit
    df['ml'] = min_loss
    df['be'] = break_even
    df['volume'] = volume
    df['commission'] = commission
    df['rror'] = df.mp / -df.ml
    
    return df[df.be < (0.99 * price)].sort('be')
#    return filter_options('bull', prices, p, df, 0.2)


###############################################################################
#                           BEAR CALL SPREAD   
#   Calculate relavent statistics for all of the possible configurations of
#   short and long call positions and return only those that meet certain 
#   criteria ------ SEE BELOW FOR DETAILS
###############################################################################
def bear_call_spread():
    max_profit = []
    break_even = []
    min_loss = []
    short_call = []
    long_call = []
    delta = []
    commission = []
    volume = []
    
    
    strikes = []
    for i in call.index.values:
        if i[0] > (0.9 * price) and i[0] < (1.1 * price):
            strikes.append(i[0])
        
    
    for sc in strikes:
        for lc in strikes:
            if lc <= sc:
                continue
            else:
                sv = call.loc[(sc, slice(None), 'call'), 'Vol'].values[0]
                lv = call.loc[(lc, slice(None), 'call'), 'Vol'].values[0]
                
                vol = np.floor(min([sv, lv]) / 10) * 10
                
                if vol < 5:
                    continue
                
                else:            
                    sp = (call.loc[(sc, slice(None), 'call'), 'Bid'].values[0] + call.loc[(sc, slice(None), 'call'), 'Ask'].values[0]) / 2
                    lp = (call.loc[(lc, slice(None), 'call'), 'Ask'].values[0] + call.loc[(lc, slice(None), 'call'), 'Bid'].values[0]) / 2
                    
                    diff = sp - lp
                    
                    c = (12.95 + (1.25 * vol) * 2)
                    
                    mp = ((sp - lp) * 100 * vol) - c
                    be = sc + (sp - lp)
                    ml = -((lc - sc - (sp - lp)) * 100 * vol) + c
                    
                    if mp < 0:
                        continue
                    
                    else:
                        max_profit.append(mp)
                        break_even.append(be)
                        min_loss.append(ml)
                        short_call.append(sc)
                        long_call.append(lc)
                        delta.append(diff)
                        volume.append(vol)
                        commission.append(c)
                    
                    
    df = pd.DataFrame({'symbol': ([s] * len(max_profit))})
    df['expiry'] = expiry
    df['sentiment'] = 'bear'
    df['underlying_price'] = price
    df['sc'] = short_call
    df['lc'] = long_call
    df['delta'] = delta
    df['mp'] = max_profit
    df['ml'] = min_loss
    df['be'] = break_even
    df['volume'] = volume
    df['commission'] = commission
    df['rror'] = df.mp / -df.ml
    
    return df[df.be > (1.01 * price)].sort('be')    
#    return filter_options('bear', prices, p, df, 0.2)


###############################################################################
#                   Profitability considering Commission
###############################################################################
def commission(symbol, options, sentiment, u_price, expiry):
    options['symbol'] = symbol
    options['sentiment'] = sentiment
    options['price'] = u_price
    options['expiry'] = expiry
    options['vol'] = 0
    options['commission'] = 0
    
    for i in range(len(options)):
                
            
        v1 = options['sv'].iloc[i]
        v2 = options['lv'].iloc[i]
        
        min_vol = min([v1,v2])
        options.vol.iloc[i] = np.floor(min_vol / 10) * 10
        
        mp = options.mp.iloc[i]
        ml = options.ml.iloc[i]
        
        c = (12.95 + (1.25 * min_vol) * 2)
        options.commission.iloc[i] = c
        
        p = (mp * min_vol) - c
        l = (ml * min_vol) - c
        
        options.mp.iloc[i] = p
        options.ml.iloc[i] = l
        
        options.rror.iloc[i] = (p / -l)
        
    options = options.drop(['sv', 'lv'], axis = 1)
    
    return options
         

###############################################################################
#           Calculate Best Options for multiple indexes and secruities
###############################################################################

securities = ['spy', 'iwm', 'qqq', 'aapl', 'nflx', 'kmx']

for s in securities:
    try:   
        opt = Options(s, 'yahoo')
    
        today = datetime.datetime.today()
        today = datetime.date(today.year, today.month, today.day)
        for e in opt.expiry_dates:
            if (e - today).days > 4 and (e - today).days < 15:
                expiry = e
        
        
        call = opt.get_call_data(expiry=expiry)
        
        price = call.Underlying_Price[0]
        
        
        
        prices, p = cdf(s, expiry, price)
        
        
        bull = bull_call_spread()
        if bull.empty:
            print('%s is Empty' %s)
        else:            
            print(filter_options('bull', prices, p, bull[bull.rror > 0.1], 0.3))
        
        bear = bear_call_spread()
        if bear.empty:
            print('%s is Empty' %s)
        else:            
            print(filter_options('bear', prices, p, bear[bear.rror > 0.1], 0.3))
        
        
    except Exception:
        continue





































