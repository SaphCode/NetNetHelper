import datetime
from .screener import Screener
from .ghost import Time

class ValueScreener(Screener):

    def __init__(self, driver, ghost):
        super().__init__(driver, ghost)

    def screen(self):
        screen = [
            # ROIC >= 20% last 5 years
            # Wenig debt
            #
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
