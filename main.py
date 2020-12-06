from screener import Screener
from excel_handler import ExcelHandler
from selenium import webdriver
import os
import time
from browser import getDriver


Ghost ghost = Ghost()
proxy = ghost.getProxy()

ip = proxy[0]
port = proxy[1]

selenium_proxy = "{ip}:{port}".format(ip=ip, port=port)
driver = getDriver(headlessMode=True, proxy=selenium_proxy)

fullName = ghost.getFullName()
firstName, lastName = fullName.split(' ')
username = ghost.getUsername(fullName)
email = ghost.getEmail()
password = 'Iwanttohaveacat90'

screener = Screener(driver)
try:
    screener.login(username, password)
except:
    screener.register(firstName, lastName, username, email, password)
screener.free_continue()
screener.init_screen(driver)
# time.sleep(3)
# screener.load_screen()
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



working_directory = os.path.join(os.path.expanduser('~'), 'OneDrive/Documents/Programming/Stocks/NetNets')
excel_handler = ExcelHandler(working_directory)
files_parent, files = excel_handler.locate_excel()
excel_handler.move_to_wd(files_parent, files)
#excel_handler.join_data()
#excel_handler.get_master_sheet()
