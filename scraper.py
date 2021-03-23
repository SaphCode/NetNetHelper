import configparser

from scraper.netnetscreener import NetNetScreener
from scraper.smallcapscreener import SmallCapScreener
from scraper.netnetanalyst import NetNetAnalyst
from scraper.smallcapanalyst import SmallCapAnalyst

from scraper.ghost import Ghost
from scraper.browser import getDriver

from datahandler.excel_handler import ExcelHandler

def getAnalystFromConfig(config, df):
    mode = config["general"]["mode"]
    if mode == "netnet":
        return NetNetAnalyst(df)
    elif mode == "smallcap":
        return SmallCapAnalyst(df)
    elif mode == "value":
        return ValueAnalyst(df)
    else:
        print("I don't have that mode programmed. Have you typed it correctly in config.ini?")
        raise Exception()

def getWDFromConfig(config):
    mode = config["general"]["mode"]
    wd = config["pc_specific"]["wd"]
    if mode == "netnet":
        return wd + "/NetNets"
    elif mode == "smallcap":
        return wd + "/SmallCap"
    elif mode == "value":
        return wd + "/Value"
    else:
        print("I don't have that mode programmed. Have you typed it correctly in config.ini?")
        raise Exception()

def getScreenerFromConfig(config, driver, ghost):
    mode = config["general"]["mode"]
    if mode == "netnet":
        return NetNetScreener(driver, ghost)
    elif mode == "smallcap":
        return SmallCapScreener(driver, ghost)
    elif mode == "value":
        return ValueScreener(driver, ghost)
    else:
        print("I don't have that mode programmed. Have you typed it correctly in config.ini?")
        raise Exception()

def main():
    config = configparser.ConfigParser()
    config.read("config.ini")

    mode = config["general"]["mode"]

    key = "undefined"
    while key != "y" and key != "n":
        key = input("Do you want to re-download all? (y/n)\n")

    if key == "y":
        ghost = Ghost()
        driver = getDriver(headlessMode=False)

        wd = getWDFromConfig(config)
        screener = getScreenerFromConfig(config, driver, ghost)

        username = config["account"]["username"]
        password = config["account"]["password"]

        screener.login(username, password) # config
        screener.screen()
        screener.getData()

        driver.close()


    key = "undefined"
    while key != "y" and key != "n":
        key = input("Do you want to process the downloaded data now? (y/n)\n")
    if key == "y":
        wd = getWDFromConfig(config)

        excel_handler = ExcelHandler(wd)
        df = excel_handler.handle()

        analyst = getAnalystFromConfig(config, df)

        filename = config["general"]["mode"]
        analyst.analyze(wd, filename)


if __name__ == '__main__':
    main()
