from screener import Screener
from excel_handler import ExcelHandler
from selenium import webdriver
from ghost import Time, Ghost
import os
import time
from browser import getDriver


key = input("Do you want to re-download all? (y/n)\n")
while key != "y" and key != "n":
    key = input("Do you want to re-download all? (y/n)\n")

if key == "y":

    ghost = Ghost()
    #ghost.wait(Time.SMALL)
    #proxy = ghost.getProxy('http://10minutemail.com/'

    #email = ghost.getEmail()



    #proxy = ghost.getProxy('http://screener.co/')
    #ip = proxy[0]
    #port = proxy[1]

    #selenium_proxy = "{ip}:{port}".format(ip=ip, port=port)

    driver = getDriver(headlessMode=False)# , proxy=selenium_proxy

    #fullName = ghost.getFullName()
    #firstName, lastName = fullName.split(' ')
    username = "drdre9696"#ghost.getUsername(fullName)
    password = "nyancat666"

    screener = Screener(driver, ghost)
    #screener.register(firstName, lastName, username, email, password)
    try:
        screener.login(username, password)
    except:
        screener.register(firstName, lastName, username, email, password)
    screener.free_continue()
    screener.init_screen(driver)

    #screener.load_screen()
    time.sleep(5)

    screener.delete_all_columns()
    time.sleep(2)
    screener.format_EBT()
    time.sleep(2)
    screener.download(0)

    time.sleep(5)


    screener.delete_all_columns()
    time.sleep(2)
    screener.format_balance_sheet()
    time.sleep(2)
    screener.download(0)


    time.sleep(5)

    screener.delete_all_columns()
    time.sleep(2)
    screener.format_descriptive()
    time.sleep(2)
    screener.download(0)

    driver.close()
    time.sleep(5) #wait for download to finish

key = "c"
key = input("Do you want to process downloaded data right now? (y/n)\n")

while key != "y" and key != "n":
    key = input("Do you want to process downloaded data right now? (y/n)\n")

if key == "y":
    working_directory = 'E:/Programming/Data/Stocks/NetNets'
    excel_handler = ExcelHandler(working_directory)
    files_parent, files = excel_handler.locate_excel()
    excel_handler.move_to_wd(files_parent, files)
    excel_handler.join_data()
    excel_handler.get_master_sheet()
