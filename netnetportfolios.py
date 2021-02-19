from portfolio.candidate_builder import *
from portfolio.portfolio_builder import *
from portfolio.portfolio_evaluater import *
from scraper.stockprice import *

def update_prices(inFile, outFile):
    bought = pd.read_csv(inFile).set_index(["Ticker", "Name"])

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
    y_tickers = []
    buy_dates = []
    portfolio = {
        'Ticker': [],
        'Name': [],
        'AdjBuy': [],
        'AdjNow': []
    }
    for ticker, name in bought.index:
        y_tickers.append(convert_to_yticker(ticker))
        buy_dates.append(get_buydate(ticker, name))
        portfolio['Ticker'].append(ticker)
        portfolio['Name'].append(name)

    for t, buyDate in zip(y_tickers, buy_dates):
        portfolio['AdjNow'].append(getPrice(t, date.today()))
        portfolio['AdjBuy'].append(getPrice(t, buyDate))

    pd.DataFrame(portfolio).set_index(["Ticker", "Name"]).to_csv(outFile)


def makeCustomPortfolios(parentDir):
    # all on nopelist
    portfolio = candidates.loc[candidates["on_nopelist"] == True]
    portfolio.to_csv(f"{parentDir}/portfolio1.csv")

    # all not on nopelist
    portfolio = candidates.loc[candidates["on_nopelist"] == False]
    portfolio.to_csv(f"{parentDir}/portfolio2.csv")

    # 10 random stocks
    for it in range(10):
        sample = random.sample(list(candidates.index), 10)
        portfolio = candidates.loc[sample]
        portfolio.to_csv(f"{parentDir}/portfolio3_{it}.csv")

    # 5 random stocks
    for it in range(10):
        sample = random.sample(list(candidates.index), 5)
        portfolio = candidates.loc[sample]
        portfolio.to_csv(f"{parentDir}/portfolio4_{it}.csv")

    # 15 random stocks
    for it in range(10):
        sample = random.sample(list(candidates.index), 15)
        portfolio = candidates.loc[sample]
        portfolio.to_csv(f"{parentDir}/portfolio5_{it}.csv")

    # 20 random stocks
    for it in range(10):
        sample = random.sample(list(candidates.index), 20)
        portfolio = candidates.loc[sample]
        portfolio.to_csv(f"{parentDir}/portfolio6_{it}.csv")


def main():

    portfolio_for = "February 2021"
    all_portfolio_folders = [
        "February 2021"
    ]

    candidates = buildCandidateList() # this builds candidates with features such as on_nopelist
    buyAll(candidates, "bought_netNets.csv") # This updates a list of all bought companies and registers the buy date

    makeCustomPortfolios(portfolio_for)

    update_prices("bought_netNets.csv", "masterPortfolio_netNets.csv") # this updates all prices of buy date and now
    # (this needs to be done because stock splits can change past prices, therefore take adjusted)

    update_portfolios(all_portfolio_folders) # this propagates the new information to all portfolios

    evaluate_portfolios(all_portfolio_folders) # this evaluates the performance of portfolios


if __name__ == "__main__":
    main()
