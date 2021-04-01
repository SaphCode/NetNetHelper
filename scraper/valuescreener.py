import datetime
from .screener import Screener
from .ghost import Time

class ValueScreener(Screener):

    def __init__(self, driver, ghost):
        super().__init__(driver, ghost)

    def screen(self):
        screen = [
            "Total debt/total equity-most recent quarter <= 0.5",
            "Return on investment-5 year average >= 0.2"
        ]

        for condition in screen:
            self.click(self.btn_create_free_form_condition, Time.SMALL)
            self.send_keys(self.input_free_form_condition, condition, Time.LONG)
            self.click(self.btn_save_free_form_condition, Time.SMALL)

        self.exclude_dark()

    def getData(self):
        self.downloadDescriptive()
