from scraper.screener import Screener
from datahandler.excel_handler import ExcelHandler
from selenium import webdriver
from scraper.ghost import Time, Ghost
import os
import time
from scraper.browser import getDriver

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

def process_data(working_directory):
    excel_handler = ExcelHandler(working_directory)
    files_parent, files = excel_handler.locate_excel()
    excel_handler.move_to_wd(files_parent, files)
    excel_handler.join_data()
    excel_handler.get_master_sheet()

def main():

    key = input("Do you want to re-download all? (y/n)\n")
    while key != "y" and key != "n":
        key = input("Do you want to re-download all? (y/n)\n")

    if key == "y":

        ghost = Ghost()
        driver = getDriver(headlessMode=False)
        screener = Screener(driver, ghost)

        login(screener, "AntonEnton99", "psychoscheiß666")

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
