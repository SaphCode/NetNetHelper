from datahandler.labels import Labels
from .analyst import Analyst
import numpy as np

class SmallCapAnalyst(Analyst):

    def __init__(self, df):
        super().__init__(df)
        self.drop_conditions = []

    def calculate_score(self):
        score = np.where(self.df[Labels.mcap]/self.df[Labels.avg_10y_ebt] > 0, self.df[Labels.mcap]/self.df[Labels.avg_10y_ebt], 10000)
        return score
