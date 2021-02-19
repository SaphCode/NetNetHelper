import pandas as pd
import numpy as np

def buildCandidateList(candidateSheet, infoSheet):
    netnets = pd.read_excel("Net Nets.xlsx", engine = 'openpyxl')
    netnets.drop(["Looked at", "Last Annual Filing", "Score"], axis = 1, inplace = True)
    netnets.set_index(["Symbol", "Company Name"], inplace = True)

    infosheet = pd.ExcelFile("TOP SECRET.xls", engine = 'openpyxl')
    nopelist = pd.read_excel(infosheet, "Nopelist")
    nopelist.set_index(["Symbol", "Company Name"], inplace = True)
    notpossible = pd.read_excel(infosheet, "Not possible List")
    notpossible = list(notpossible["Exchange"])


    netnets["on_nopelist"] = [True if (ticker, name) in nopelist.index else False for ticker, name in netnets.index]
    netnets["exchange"] = [ticker.split(':')[0] for ticker, name in netnets.index]
    canBuy = [False if ticker.split(':')[0] in notpossible or ticker.split(':')[0] == "VSE" else True for ticker, name in netnets.index]
    candidates = netnets.loc[canBuy]


    candidates["avg10yEBT/NCAV"] = candidates["AVG 10y EBT"]/candidates["NCAV"]
    candidates["assets/NCAV"] = candidates["Total Assets"]/candidates["NCAV"]
    candidates["liabilities/assets"] = candidates["Total Liabilities"]/candidates["Total Assets"]
    candidates["cash/NCAV"] = candidates["Cash & Equivalents"]/candidates["NCAV"]
    candidates["receivables/NCAV"] = candidates["Receivables"]/candidates["NCAV"]
    candidates["inventory/NCAV"] = candidates["Inventory"]/candidates["NCAV"]
    candidates["med5yebt/NCAV"] = candidates["Median EBT 5y"]/candidates["NCAV"]
    candidates["med10yebt/NCAV"] = candidates["Median EBT 10y"]/candidates["NCAV"]

    candidates.drop(["NCAV", "Median EBT 10y", "AVG 10y EBT",
                     "Total Assets", "Total Liabilities", "Cash & Equivalents",
                     "Receivables", "Inventory", "10y Earnings Yield",
                     "Earnings Trend", "3y AVG EBT", "Median EBT 5y",
                     "EBT A-5", "EBT A-6", "EBT A-7",
                     "EBT A-8", "EBT A-9"], axis = 1, inplace = True)

    return candidates
    #candidates.dropna(axis = 0, inplace = True)

    #one = PCA(n_components = 2).fit(candidates)
    #print(one.explained_variance_ratio_)

    #clusters = KMeans(n_clusters = 2).fit(candidates)
    #candidates["cluster"] = clusters.labels_
    #candidates
    #>candidates = (candidates - candidates.min()) / (candidates.max() - candidates.min())
