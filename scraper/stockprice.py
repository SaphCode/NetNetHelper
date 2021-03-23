from yahoofinancials import YahooFinancials
from datetime import date, timedelta

def convert_to_yticker(ticker):
    exchange_dict = {
        'HKG': '.HK',
        'SIN': '.SI',
        'TYO': '.T',
        'SWF': '.SW',
        'STO': '.ST',
        'CVE': '.V',
        'NASD': '',
        'OTC': ''
    }
    y_ticker = ticker.split(':')[1] + exchange_dict[ticker.split(':')[0]]
    if ('.HK' in y_ticker):
        y_ticker = y_ticker.zfill(7)
    return y_ticker

def getPrice(ticker, wanted_date):
    yf = YahooFinancials(ticker)
    before_wanted_date = wanted_date - timedelta(days = 5)
    data = yf.get_historical_price_data(before_wanted_date.strftime("%Y-%m-%d"), wanted_date.strftime("%Y-%m-%d"), 'monthly')
    stock_data = data[ticker]
    price = 0
    try:
        price_data = stock_data['prices'][0]
        adj_close = price_data['adjclose']
        price = adj_close
    except:
        print(f'Ticker {t} not found, using default price 0.')
    return price
