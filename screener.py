from selenium import webdriver
import logging
import os
import time
import math
from ghost import Time, Ghost

class Screener:

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


    def click(self, xpath, time):
        self.ghost.wait(time)
        self.driver.find_element_by_xpath(xpath).click()


    def send_keys(self, xpath, keys, time):
        self.ghost.wait(time)
        self.driver.find_element_by_xpath(xpath).send_keys(keys)


    def init_screen(self, driver):
        create_free_form_btn = '/html/body/div[2]/div[2]/div/div[4]/table/tbody/tr[3]/td/div/div[3]/div/div[2]/div/table/tbody/tr[1]/td/div/div[3]'
        self.click(create_free_form_btn, Time.MEDIUM)
        screen = 'Cash and Equiv.-most recent quarter + 0.75 * Receivables-most recent quarter + 0.5 * Inventory-most recent quarter - Liabilities, total-most recent quarter > Market capitalization'
        input = '/html/body/div[3]/div/table/tbody/tr[2]/td[2]/div/div/input[1]'
        self.click(input, Time.VERY_SMALL)
        self.send_keys(input, screen, Time.LONG)
        save_btn = '/html/body/div[3]/div/table/tbody/tr[2]/td[2]/div/div/div[3]'
        self.click(save_btn, Time.VERY_SMALL)
        #cancel_btn = '/html/body/div[3]/div/table/tbody/tr[2]/td[2]/div/div/div[2]'
        #self.click(cancel_btn, Time.VERY_SMALL)


    def register(self, firstName, lastName, username, email, password):
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


    def login(self, username, password):
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


    def free_continue(self):
        continue_btn = '/html/body/div[4]/div/table/tbody/tr[2]/td[2]/div/div/div[2]/div'
        self.click(continue_btn, Time.LONG)


    def load_screen(self):
        xpath_screens = '/html/body/div[2]/div[2]/div/div[4]/table/tbody/tr[1]/td/div/table/tbody/tr/td[3]'
        xpath_loadScreen = '/html/body/div[3]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[1]/td'
        xpath_folder = '/html/body/div[3]/div/table/tbody/tr[2]/td[2]/div/div/div[4]/div[3]/div/div/div/div/div[1]/div[6]'
        xpath_screen = '/html/body/div[3]/div/table/tbody/tr[2]/td[2]/div/div/div[4]/div[5]/div/div/div/div/div[1]/div[2]'
        xpath_loadScreenBtn = '/html/body/div[3]/div/table/tbody/tr[2]/td[2]/div/div/div[2]'
        self.click(xpath_screens, Time.MEDIUM)
        self.click(xpath_loadScreen, Time.VERY_SMALL)
        self.click(xpath_folder, Time.VERY_SMALL)
        self.click(xpath_screen, Time.SMALL)
        self.click(xpath_loadScreenBtn, Time.VERY_SMALL)


    ## max_downloads = maximum amount of companies to download, 0 to download all
    def download(self, max_downloads):
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


    def __hover(self, xpath, time):
        self.ghost.wait(time)
        element = self.driver.find_element_by_xpath(xpath)
        hover = webdriver.ActionChains(self.driver).move_to_element(element)
        hover.perform()


    def format_EBT(self):
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
            self.__hover(xpath_incomeStatement, Time.SMALL)
            self.__hover(xpath_A, Time.SMALL)
            self.__hover(xpath_last_item, Time.SMALL)
            #self.__hover(xpath_EBT)
            #self.__hover(xpath_A) # double b/c of scrolling issues
            #self.__hover(xpath_EBT) # double b/c of scrolling issues
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
            self.__hover(xpath_expandedHistory, Time.SMALL)
            self.__hover(xpath_expandedIncomeStatement, Time.SMALL)
            self.__hover(xpath_expandedA, Time.SMALL)
            #self.__hover(xpath_last_item)
            #self.__hover(xpath_expandedA)
            #self.__hover(xpath_expandedA)
            #self.__hover(xpath_expandedA)
            self.__hover(xpath_expandedEBT, Time.SMALL) # double b/c of scrolling issues
            self.__hover(xpath_expandedA, Time.SMALL)
            # self.__hover(xpath_expandedA)
            # self.__hover(xpath_expandedEBT)
            self.click(xpath_expandedEBT, Time.SMALL)

        '''WORKING A9 ON LINUX GOOGLE CHROME (NOT CHROMIUM)'''
        xpath_expandedA = '/html/body/div[5]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[{}]/td[1]'.format(pos_A_9)
        xpath_last_item = '/html/body/div[6]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[23]/td'
        self.click(xpath_columns, Time.MEDIUM)
        self.__hover(xpath_expandedHistory, Time.SMALL)
        self.__hover(xpath_expandedIncomeStatement, Time.SMALL)
        self.__hover(xpath_expandedA, Time.SMALL)
        self.__hover(xpath_expandedA, Time.MEDIUM)
        self.__hover('/html/body/div[6]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[1]/td', Time.SMALL)
        self.click(xpath_expandedEBT, Time.SMALL)

        self.logger.info('Added all EBT columns.')


    def format_balance_sheet(self):
        self.logger.info('Adding balance sheet columns ...')
        columns = [1, 2, 3, 5, 7, 8, 9, 10, 14]
        xpath_columns = '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/div/table/tbody/tr/td[1]'
        xpath_balanceSheet = '/html/body/div[3]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[7]/td[1]'
        xpath_mrq = '/html/body/div[4]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[6]/td[1]'
        for i in columns:
            xpath_ithElement = '/html/body/div[5]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr[' + str(i) + ']/td'

            self.click(xpath_columns, Time.SMALL)
            self.__hover(xpath_balanceSheet, Time.SMALL)
            self.__hover(xpath_mrq, Time.SMALL)
            self.__hover(xpath_balanceSheet, Time.VERY_SMALL)
            self.__hover(xpath_mrq, Time.SMALL)
            self.click(xpath_ithElement, Time.SMALL)

        self.logger.info('Added balance sheet columns!')


    def format_descriptive(self):
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
        self.__hover(xpath_shareRelated, Time.SMALL)
        self.click(xpath_marketCap, Time.SMALL)

        self.click(xpath_columns, Time.LONG)
        self.__hover(xpath_descriptive, Time.SMALL)
        self.__hover(xpath_exchRates, Time.SMALL)
        self.click(xpath_priceToFinancialReportingCurrency, Time.SMALL)

        self.click(xpath_columns, Time.MEDIUM)
        self.__hover(xpath_descriptive, Time.SMALL)
        self.__hover(xpath_exchRates, Time.SMALL)
        self.click(xpath_exchRateReportingToUSD, Time.SMALL)

        self.click(xpath_columns, Time.SMALL)
        self.__hover(xpath_descriptive, Time.SMALL)
        self.__hover(xpath_filingInformation, Time.SMALL)
        self.click(xpath_lastAnnualFiling, Time.SMALL)

        self.logger.info('Added descriptive columns!')
