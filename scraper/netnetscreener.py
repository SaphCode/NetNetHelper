from .screener import Screener
from .ghost import Time

class NetNetScreener(Screener):

    def __init__(self, driver, ghost):
        super().__init__(driver, ghost)

    def screen(self):
        screen = 'Cash and Equiv.-most recent quarter + 0.75 * Receivables-most recent quarter + 0.5 * Inventory-most recent quarter - Liabilities, total-most recent quarter > Market capitalization'

        self.click(self.btn_create_free_form_condition, Time.MEDIUM)
        self.send_keys(self.input_free_form_condition, screen, Time.LONG)
        self.click(self.btn_save_free_form_condition, Time.VERY_SMALL)

        self.exclude_dark()
