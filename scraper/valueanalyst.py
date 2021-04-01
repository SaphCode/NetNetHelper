from datahandler.labels import Labels
from .analyst import Analyst

class ValueAnalyst(Analyst):

    def __init__(self, df):
        super().__init__(df)
        self.drop_conditions = []

    def calculate_score(self):
        score = self.df[Labels.mcap]
        print('Calculated score.')
        return score
