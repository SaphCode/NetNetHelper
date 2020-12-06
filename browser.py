from selenium import webdriver
from sys import platform
import os

def getDriver(headlessMode, proxy):
    chrome_options = webdriver.ChromeOptions()#chrome.options.Options()
    if proxy:
        desired_capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        desired_capabilities['proxy'] = {
            "httpProxy": proxy,
            "ftpProxy": proxy,
            "sslProxy": proxy,
            "noProxy": None,
            "proxyType": "MANUAL",
            "class": "org.openqa.selenium.Proxy",
            "autodetect": False
        }
        #chrome_options.add_argument('--proxy-server={}'.format(proxy))
    if headlessMode:
        chrome_options.add_argument('headless')
    path = 'driver/'
    driver = None
    if platform == 'linux' or platform == 'linux2':
        path += 'chromedriver'
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()

        # chrome_options.add_experimental_option("useAutomationExtension", False)
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument("--remote-debugging-port=9222")


        #chrome_options.add_argument("--headless")

        #path += 'geckodriver'
    else:
        path += 'chromedriver.exe'
        driver = webdriver.Chrome(executable_path=os.path.abspath(path), options=chrome_options) #, options=chrome_options)

        driver.set_window_size(974, 1047)
        driver.set_window_position(953, 0)
    if not driver:
        raise Exception("Not running on windows or linux.. no driver selected.")
    return driver
