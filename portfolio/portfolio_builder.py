import pandas as pd
import numpy as np
from yahoofinancials import YahooFinancials
from datetime import date, timedelta
import glob

def buyAll(candidates, outFile):
    now = date.today()
    bought_now = {
        'Ticker': [],
        'Name': [],
        'BuyDate': []
    }
    for ticker, name in candidates.index:
        bought_now['Ticker'].append(ticker)
        bought_now['Name'].append(name)
        bought_now['BuyDate'].append(now)
    bought_now = pd.DataFrame(bought_now)

    filename = outFile
    bought = pd.read_csv(filename)
    updated = pd.concat([bought, bought_now]).drop_duplicates(subset = ['Ticker', 'Name'], keep = 'first').set_index(['Ticker', 'Name'])
    updated['BuyDate'] = pd.to_datetime(updated['BuyDate'])
    updated.to_csv(filename)

def get_buydate(ticker, name):
    bought = pd.read_csv("bought.csv")
    bought.set_index(["Ticker", "Name"], inplace = True)
    bought['BuyDate'] = pd.to_datetime(bought['BuyDate'])
    buy_date = bought['BuyDate'].loc[(ticker, name)]
    return buy_date



def update_portfolios():
    fnames = glob.glob("Portfolios/portfolio*.csv")
    master_portfolio = pd.read_csv("master_portfolio.csv")
    for fname in fnames:
        p = pd.read_csv(fname).set_index(['Symbol', 'Company Name'])
        subset = master_portfolio.loc[p.index]
        p['AdjBuyPrice'] = subset['AdjBuy']
        p['AdjNowPrice'] = subset['AdjNow']
        p.to_csv(fname)
