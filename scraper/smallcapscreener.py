import datetime
from .screener import Screener
from .ghost import Time

class SmallCapScreener(Screener):

    def __init__(self, driver, ghost):
        super().__init__(driver, ghost)

    def screen(self):
        screen = [
            f'Market Capitalization < {5*10**6}',
            f'Volume-avg. trading volume for the last 3 months > 0',
            #f'Last annual filing >= {critical_date.strftime("%m/%d/%Y")}',
            'Current ratio-most recent quarter > 1.5'
        ]

        for condition in screen:
            self.click(self.btn_create_free_form_condition, Time.SMALL)
            self.send_keys(self.input_free_form_condition, condition, Time.LONG)
            self.click(self.btn_save_free_form_condition, Time.SMALL)

        self.exclude_dark()

    def getData(self):
        self.downloadEarnings()
        self.downloadBalanceSheet()
        self.downloadDescriptive()
