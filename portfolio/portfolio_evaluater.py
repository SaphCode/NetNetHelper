import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

def evaluate_portfolios():
    fnames = glob.glob(f"{portfolio_for}/portfolio*.csv")
    print(fnames)
    gains = {
        'fname': fnames,
        '%gain': []
    }
    for fname in fnames:
        p = pd.read_csv(fname).set_index(['Symbol', 'Company Name'])
        p['%Change'] = p['AdjNow']/p['AdjBuy']
        gains['%change'].append(p["%Change"].mean()) # skipna true by default
        print(f'Portfolio {fname.split("portfolio")[1].replace(".csv", "")} had a %-change of {p["%Change"].mean()}')
    np_gains = np.array(gains['%gain'])
    print(np_gains)
    plt.boxplot(np_gains)
    plt.show()
