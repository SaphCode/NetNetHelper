from abc import ABC, abstractmethod

from .ghost import Time

import logging
import time
import math
import os
import datetime

from selenium import webdriver
from selenium.webdriver.support.ui import Select


class Screener(ABC):
    """Abstract Base class for screeners."""

    def __init__(self, driver, ghost):
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(pathname)s - %(lineno)d: %(message)s')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        logger_fh = logging.FileHandler('log/screener_download.log')
        logger_fh.setLevel(logging.WARNING)
        logger_fh.setFormatter(formatter)

        logger_ch = logging.StreamHandler()
        logger_ch.setLevel(logging.DEBUG)
        logger_ch.setFormatter(formatter)

        self.logger.addHandler(logger_fh)
        self.logger.addHandler(logger_ch)

        self.driver = driver

        self.register_page = 'https://screener.co/'
        self.login_page = 'https://stock.screener.co/'

        self.ghost = ghost

        self.dummy_text = '/html/body/div[3]/div/table/tbody/tr[2]/td[2]/div/div/div[1]'

        self.btn_free_continue = '/html/body/div[4]/div/table/tbody/tr[2]/td[2]/div/div/div[2]/div'

        self.btn_create_free_form_condition = '/html/body/div[2]/div[2]/div/div[4]/table/tbody/tr[3]/td/div/div[3]/div/div[2]/div/table/tbody/tr[1]/td/div/div[3]'
        self.input_free_form_condition = '/html/body/div[3]/div/table/tbody/tr[2]/td[2]/div/div/input[1]'
        self.btn_save_free_form_condition = '/html/body/div[3]/div/table/tbody/tr[2]/td[2]/div/div/div[3]'

        self.btn_add_screen_condition = '/html/body/div[2]/div[2]/div/div[4]/table/tbody/tr[3]/td/div/div[3]/div/div[2]/div/table/tbody/tr[1]/td/div/div[1]/table/tbody/tr/td'
        self.dropdown_screen_condition = '/html/body/div[3]/div/table/tbody/tr[2]/td[2]/div/div/select'
        self.input_screen_condition = '/html/body/div[3]/div/table/tbody/tr[2]/td[2]/div/div/input'
        self.btn_save_screen_condition = '/html/body/div[3]/div/table/tbody/tr[2]/td[2]/div/div/div[4]'

        self.menu_descriptive = '/html/body/div[3]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[1]/td[1]'
        self.menu_filing_info = '/html/body/div[4]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[4]/td[1]'
        self.info_last_annual_filing = '/html/body/div[5]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[2]/td'


    # NOT USED CURRENTLY
    def register(self, firstName, lastName, username, email, password):
        """Register for a new account. Deprecated."""
        self.driver.get(self.register_page)
        sign_up_btn = '/html/body/div[1]/div/div[1]/div[3]/input'
        self.click(sign_up_btn, Time.MEDIUM)
        username_prompt = '/html/body/div[2]/div/div/div/div/form/div/div/div/div/div[1]/div[2]/div[1]/input'
        password_prompt = '/html/body/div[2]/div/div/div/div/form/div/div/div/div/div[1]/div[2]/div[2]/div[1]/input'
        confirm_password_prompt = '/html/body/div[2]/div/div/div/div/form/div/div/div/div/div[1]/div[2]/div[2]/div[2]/input'
        firstName_prompt = '/html/body/div[2]/div/div/div/div/form/div/div/div/div/div[1]/div[2]/div[3]/div[1]/input'
        lastName_prompt = '/html/body/div[2]/div/div/div/div/form/div/div/div/div/div[1]/div[2]/div[3]/div[2]/input'
        email_prompt = '/html/body/div[2]/div/div/div/div/form/div/div/div/div/div[1]/div[2]/div[4]/input'
        self.send_keys(username_prompt, username, Time.MEDIUM)
        self.send_keys(password_prompt, password, Time.MEDIUM)
        self.send_keys(confirm_password_prompt, password, Time.SMALL)
        self.send_keys(firstName_prompt, firstName, Time.SMALL)
        self.send_keys(lastName_prompt, lastName, Time.MEDIUM)
        self.send_keys(email_prompt, email, Time.SMALL)

        create_acc_btn = '/html/body/div[2]/div/div/div/div/form/div/div/div/div/div[1]/div[2]/div[7]/button'

        self.click(create_acc_btn, Time.LONG)


    def login(self, username: str, password: str):
        """Login to screener.co using username and password."""
        self.logger.debug('Resolving website {}'.format(self.login_page))
        self.driver.get(self.login_page)

        self.logger.debug('Sending login info:\nUsername: {},\n Password: {}'.format(username, password))
        username_prompt_xpath = '/html/body/div[2]/div/table/tbody/tr[2]/td[2]/div/div/input[1]'
        password_prompt_xpath = '/html/body/div[2]/div/table/tbody/tr[2]/td[2]/div/div/input[2]'
        submit_button_xpath = '/html/body/div[2]/div/table/tbody/tr[2]/td[2]/div/div/div[4]/div'

        self.send_keys(username_prompt_xpath, username, Time.MEDIUM)
        self.send_keys(password_prompt_xpath, password, Time.SMALL)
        self.click(submit_button_xpath, Time.SMALL)

        self.logger.info('Login successful!')

        self.logger.info('Waiting for free continue ..')
        self.click(self.btn_free_continue, Time.LONG)

    ## max_downloads = maximum amount of companies to download, 0 to download all
    def download(self, max_downloads):
        """Downloads all results currently displayed."""
        wait_time_before_downloading = Time.LONG
        self.logger.debug('Waiting {} seconds before starting download ...'.format(wait_time_before_downloading))
        time.sleep(wait_time_before_downloading)

        results_xpath = '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[4]/td/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div'
        num_results = int(self.driver.find_element_by_xpath(results_xpath).text.split(' of ')[1])
        self.logger.info('Found {} results.'.format(num_results))

        if max_downloads != 0:
            if num_results > max_downloads:
                self.logger.warning('Not downloading all results ({} found vs {} max download)'.format(num_results, max_downloads))
        else:
            self.logger.info('Downloading all results..')

        max_results_per_page = 50
        num_pages = 0
        if max_downloads != 0:
            num_pages = int(math.ceil(max_downloads/max_results_per_page))
        else:
            num_results = int(self.driver.find_element_by_xpath(results_xpath).text.split(' of ')[1])
            num_pages = int(math.ceil(num_results / max_results_per_page))

        self.logger.debug('Number of pages to download: {}'.format(num_pages))

        download_to_excel_xpath = '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/div/table/tbody/tr/td[4]'
        next_page_xpath = '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[4]/td/table/tbody/tr[2]/td/table/tbody/tr/td[5]/button'
        for i in range(0, num_pages):
            #self.logger.debug('Waiting 1 second before downloading ...')
            self.logger.debug('Downloading page {} (results {}-{}): '.format(i+1, i*max_results_per_page + 1, (i+1)*max_results_per_page))
            self.click(download_to_excel_xpath, Time.SMALL)
            self.click(next_page_xpath, Time.VERY_SMALL)

        self.logger.info('Finished downloading, resetting to first page ..')
        xpath_back_to_first_page = '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[4]/td/table/tbody/tr[2]/td/table/tbody/tr/td[3]/button'
        self.click(xpath_back_to_first_page, Time.MEDIUM)


    def delete_all_columns(self):
        """Delete info columns from company view, to make more space for other columns."""
        self.logger.info('Deleting all columns ...')

        columns = self.driver.find_element_by_class_name('masterview-grid-header').find_elements_by_class_name('masterview-grid-header-cell')
        number_of_items = len(columns)

        #muss größer als 2 sein weil die ersten beiden nicht gelöscht werden können
        while (number_of_items > 2):
            actionChains = webdriver.ActionChains(self.driver)

            #der plan ist bei der letzten column anzufangen und von hinten nach vorne alle zu löschen
            #andere richtung funktioniert nicht weil er das element nicht findet beim zweiten druchlauf
            path = '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[4]/td/table/tbody/tr[1]/td/div/div[2]/div/table/tbody/tr/td[' + str(number_of_items) + ']/div'
            time.sleep(1)

            #wir locaten die column
            element = self.driver.find_element_by_xpath(path)

            #rechts klick
            actionChains.context_click(element).perform()

            #entfernt das elements
            self.driver.find_element_by_xpath('/html/body/div[3]/div/div/table/tbody/tr[3]/td').click()

            number_of_items -= 1
        self.logger.info('Deleted all columns!')


    def format_descriptive(self):
        """Formats the company view to include descriptive columns."""
        self.logger.info('Adding descriptive columns ...')
        xpath_columns = '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/div/table/tbody/tr/td[1]'
        xpath_descriptive = '/html/body/div[3]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[1]/td[1]'
        xpath_exchRates = '/html/body/div[4]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[6]/td[1]'
        xpath_shareRelated = '/html/body/div[3]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[14]/td[1]'
        xpath_marketCap = '/html/body/div[4]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[3]/td'
        xpath_priceToFinancialReportingCurrency = '/html/body/div[5]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[1]/td'
        xpath_exchRateReportingToUSD = '/html/body/div[5]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[2]/td'
        xpath_filingInformation = '/html/body/div[4]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[4]/td[1]'
        xpath_lastAnnualFiling = '/html/body/div[5]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[2]/td'

        self.click(xpath_columns, Time.MEDIUM)
        self.hover(xpath_shareRelated, Time.SMALL)
        self.click(xpath_marketCap, Time.SMALL)

        self.click(xpath_columns, Time.LONG)
        self.hover(xpath_descriptive, Time.SMALL)
        self.hover(xpath_exchRates, Time.SMALL)
        self.click(xpath_priceToFinancialReportingCurrency, Time.SMALL)

        self.click(xpath_columns, Time.MEDIUM)
        self.hover(xpath_descriptive, Time.SMALL)
        self.hover(xpath_exchRates, Time.SMALL)
        self.click(xpath_exchRateReportingToUSD, Time.SMALL)

        self.click(xpath_columns, Time.SMALL)
        self.hover(xpath_descriptive, Time.SMALL)
        self.hover(xpath_filingInformation, Time.SMALL)
        self.click(xpath_lastAnnualFiling, Time.SMALL)

        self.logger.info('Added descriptive columns!')


    def format_balance_sheet(self):
        """Formats the company view to include balance sheet criteria."""
        self.logger.info('Adding balance sheet columns ...')
        columns = [1, 2, 3, 5, 7, 8, 9, 10, 14]
        xpath_columns = '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/div/table/tbody/tr/td[1]'
        xpath_balanceSheet = '/html/body/div[3]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[7]/td[1]'
        xpath_mrq = '/html/body/div[4]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[6]/td[1]'
        for i in columns:
            xpath_ithElement = '/html/body/div[5]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[' + str(i) + ']/td'

            self.click(xpath_columns, Time.SMALL)
            self.hover(xpath_balanceSheet, Time.SMALL)
            self.hover(xpath_mrq, Time.SMALL)
            self.hover(xpath_balanceSheet, Time.VERY_SMALL)
            self.hover(xpath_mrq, Time.SMALL)
            self.click(xpath_ithElement, Time.SMALL)

        self.logger.info('Added balance sheet columns!')


    def format_EBT(self):
        """Formats the company view to have all EBT from the last 10 years, to get ready for download."""
        self.logger.info('Adding all EBT columns ...')
        #A - A-4
        self.logger.debug('Going into income statement ..')
        pos_A = 13
        pos_A_4 = 17
        xpath_columns = '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/div/table/tbody/tr/td[1]'
        xpath_incomeStatement = '/html/body/div[3]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[6]/td[1]'
        xpath_EBT = '/html/body/div[5]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[10]/td'
        for i in range(pos_A, pos_A_4+1):
            xpath_A = '/html/body/div[4]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[' + str(i) + ']/td[1]'
            xpath_last_item = '/html/body/div[5]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[20]/td'
            self.click(xpath_columns, Time.SMALL)
            self.hover(xpath_incomeStatement, Time.SMALL)
            self.hover(xpath_A, Time.SMALL)
            self.hover(xpath_last_item, Time.SMALL)
            #self.hover(xpath_EBT)
            #self.hover(xpath_A) # double b/c of scrolling issues
            #self.hover(xpath_EBT) # double b/c of scrolling issues
            self.click(xpath_EBT, Time.SMALL)

        self.logger.debug('Going into expanded history > income statement ..')
        pos_A_5 = 1
        pos_A_9 = 5
        xpath_expandedHistory = '/html/body/div[3]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[19]/td[1]'
        xpath_expandedIncomeStatement = '/html/body/div[4]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[1]/td[1]'
        xpath_expandedEBT = '/html/body/div[6]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[10]/td'
        for i in range(pos_A_5, pos_A_9):
            '''DO A9 SEPARATELY, DOESNT WORK IN THIS LOOP'''
            xpath_expandedA = '/html/body/div[5]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[' + str(i) + ']/td[1]'

            self.driver.find_element_by_xpath(xpath_columns).click()
            self.hover(xpath_expandedHistory, Time.SMALL)
            self.hover(xpath_expandedIncomeStatement, Time.SMALL)
            self.hover(xpath_expandedA, Time.SMALL)
            #self.hover(xpath_last_item)
            #self.hover(xpath_expandedA)
            #self.hover(xpath_expandedA)
            #self.hover(xpath_expandedA)
            self.hover(xpath_expandedEBT, Time.SMALL) # double b/c of scrolling issues
            self.hover(xpath_expandedA, Time.SMALL)
            # self.hover(xpath_expandedA)
            # self.hover(xpath_expandedEBT)
            self.click(xpath_expandedEBT, Time.SMALL)

        '''WORKING A9 ON LINUX GOOGLE CHROME (NOT CHROMIUM)'''
        xpath_expandedA = '/html/body/div[5]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[{}]/td[1]'.format(pos_A_9)
        xpath_last_item = '/html/body/div[6]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[23]/td'
        self.click(xpath_columns, Time.MEDIUM)
        self.hover(xpath_expandedHistory, Time.SMALL)
        self.hover(xpath_expandedIncomeStatement, Time.SMALL)
        self.hover(xpath_expandedA, Time.SMALL)
        self.hover(xpath_expandedA, Time.MEDIUM)
        self.hover('/html/body/div[6]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[1]/td', Time.SMALL)
        self.click(xpath_expandedEBT, Time.SMALL)

        self.logger.info('Added all EBT columns.')


    def exclude_dark(self):
        """Exclude companies whose last report was >=2 years ago."""

        today = datetime.datetime.now()
        d = datetime.timedelta(days = 365 + 4*31) # 1 year & 4 months
        critical_date = today - d

        self.click(self.btn_add_screen_condition, Time.SMALL)
        self.hover(self.menu_descriptive, Time.SMALL)
        self.hover(self.menu_filing_info, Time.SMALL)
        self.click(self.info_last_annual_filing, Time.SMALL)

        self.select(self.dropdown_screen_condition, '>=', Time.MEDIUM)

        self.send_keys(self.input_screen_condition, critical_date.strftime("%m/%d/%Y"), Time.MEDIUM)

        self.click(self.dummy_text, Time.VERY_SMALL)
        self.click(self.btn_save_screen_condition, Time.SMALL)


    def hover(self, xpath: str, time: Time):
        """A helper method for hovering over menu points. Use this to navigate."""
        self.ghost.wait(time)
        element = self.driver.find_element_by_xpath(xpath)
        hover = webdriver.ActionChains(self.driver).move_to_element(element)
        hover.perform()

    def click(self, xpath: str, time: Time):
        """A helper method for clicking."""
        self.ghost.wait(time)
        self.driver.find_element_by_xpath(xpath).click()


    def send_keys(self, xpath: str, keys: str, time: Time):
        """A helper method for sending keys to an input html."""
        self.ghost.wait(time)
        element = self.driver.find_element_by_xpath(xpath)
        element.clear()
        element.send_keys(keys)

    def select(self, xpath: str, value: str, time: Time):
        """Helper method. Select field with value from dropdown, after time has elapsed."""
        self.ghost.wait(Time.MEDIUM)
        select = Select(self.driver.find_element_by_xpath(xpath))
        select.select_by_value(value)

    @abstractmethod
    def screen(self):
        """Implement your screening logic here."""
        pass
