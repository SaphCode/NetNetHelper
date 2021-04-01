from yahoofinancials import YahooFinancials
from datetime import date, timedelta

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

def convert_to_yticker(ticker):
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
        key = "undefined"
        while key != "y" and key != "n":
            key = input(f"Ticker {ticker} not found, using default price 0.\n The exchange dict used is {exchange_dict}.\nMaybe the exchange is not listed here, so we can't find it on YahooFinancials.\n Do you want to continue? (y/n)")
        if key == "n":
            print("Please fix me now")
            raise Exception()
    return price
