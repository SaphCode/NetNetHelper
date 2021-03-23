from datahandler.labels import Labels
from .analyst import Analyst

class NetNetAnalyst(Analyst):

    def __init__(self, df):
        super().__init__(df)
        self.drop_conditions = [
            ('Median 10y EBT < 0', self.df[Labels.med_10y_ebt] <= 0),
            ('Inventory > 85% NCAV', (self.df[Labels.inventory]/self.df[Labels.ncav] >= 0.85)),
            ('Receivables > 95% NCAV', (self.df[Labels.receivables]/self.df[Labels.ncav] >= 0.95)),
            ('Market Cap < 5% NCAV', self.df[Labels.mcap]/self.df[Labels.ncav] <= 0.05)
        ]


    def calculate_score(self):
        score = 1-self.df[Labels.mcap_to_ncav]
        score += self.df[Labels.earnings_yield_10y]
        score += self.df[Labels.cash]/self.df[Labels.ncav]
        score += (self.df[Labels.ncav] + self.df[Labels.total_liabilities])/self.df[Labels.total_assets]
        print('Calculated score.')
        return score
