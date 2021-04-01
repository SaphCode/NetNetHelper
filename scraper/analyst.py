from abc import ABC, abstractmethod

class Analyst(ABC):
    """Abstract base class for scrapers."""

    def __init__(self, df):
        self.df = df
        self.drop_conditions = []

    def calculate_score(self):
        """Calculates the score achieved by the companies. Use the labels from .datahandler.labels to calculate.

        The default implementation returns 0 for every company in df.
        """
        score = [0 for key in self.df.index]
        return score

    def analyze(self, working_directory: str, filename: str):
        for condition_name, condition in self.drop_conditions:
            print(condition_name)
            self.df.drop(self.df.loc[condition].index, inplace = True)
        self.df['Score'] = self.calculate_score()
        self.df = self.df.sort_values(by='Score', ascending = False)
        self.df.to_csv('{parent}/{filename}.csv'.format(parent = working_directory, filename = filename))
