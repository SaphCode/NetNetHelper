from scraper.netnetscreener import NetNetScreener
from datahandler.excel_handler import ExcelHandler
from selenium import webdriver
from scraper.ghost import Time, Ghost
import os
import time
from scraper.browser import getDriver
from datahandler.labels import Labels

def login(screener, username, password):
    try:
        screener.login(username, password)
    except:
        screener.register(firstName, lastName, username, email, password)
    screener.free_continue()

def downloadEarnings(screener):
    screener.delete_all_columns()
    time.sleep(2)
    screener.format_EBT()
    time.sleep(2)
    screener.download(0)

def downloadBalanceSheet(screener):
    screener.delete_all_columns()
    time.sleep(2)
    screener.format_balance_sheet()
    time.sleep(2)
    screener.download(0)

def downloadDescriptive(screener):
    screener.delete_all_columns()
    time.sleep(2)
    screener.format_descriptive()
    time.sleep(2)
    screener.download(0)

def calculate_score(df):
    score = 1-df[Labels.mcap_to_ncav]
    score += df[Labels.earnings_yield_10y]
    score += df[Labels.cash]/df[Labels.ncav]
    score += (df[Labels.ncav] + df[Labels.total_liabilities])/df[Labels.total_assets]
    print('Calculated score.')
    return score

def process_data(working_directory):
    excel_handler = ExcelHandler(working_directory)
    files_parent, files = excel_handler.locate_excel()
    excel_handler.move_to_wd(files_parent, files)
    excel_handler.join_data()
    master = excel_handler.get_master_sheet()
    drop_conditions = [
        ('Median 10y EBT < 0', master[Labels.med_10y_ebt] <= 0),
        ('Inventory > 85% NCAV', (master[Labels.inventory]/master[Labels.ncav] >= 0.85)),
        ('Receivables > 95% NCAV', (master[Labels.receivables]/master[Labels.ncav] >= 0.95)),
        ('Market Cap < 5% NCAV', master[Labels.mcap]/master[Labels.ncav] <= 0.05)
    ]
    for condition_name, condition in drop_conditions:
        print(condition_name)
        master.drop(master.loc[condition].index, inplace = True)
    master['Score'] = calculate_score(master)
    master = master.sort_values(by='Score', ascending = False)
    master.to_csv('{parent}/{filename}'.format(parent = working_directory, filename = 'netnets.csv'))



def main():

    key = input("Do you want to re-download all? (y/n)\n")
    while key != "y" and key != "n":
        key = input("Do you want to re-download all? (y/n)\n")

    if key == "y":

        DIRECTORY_OF_PROJECT = "E:/Programming/Projects/NetNetHelper"

        ghost = Ghost()
        driver = getDriver(DIRECTORY_OF_PROJECT, headlessMode=False)
        screener = NetNetScreener(driver, ghost)

        login(screener, "macmiller77", "BurgerMacKing55")

        screener.init_screen(driver)

        time.sleep(5)

        downloadEarnings(screener)

        time.sleep(5)

        downloadBalanceSheet(screener)

        time.sleep(5)

        downloadDescriptive(screener)

        driver.close()
        time.sleep(5) #wait for download to finish

    key = "c"
    key = input("Do you want to process downloaded data right now? (y/n)\n")

    while key != "y" and key != "n":
        key = input("Do you want to process downloaded data right now? (y/n)\n")

    if key == "y":
        process_data('E:/Programming/Data/Stocks/NetNets')

if __name__ == '__main__':
    main()
