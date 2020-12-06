import dateutil.parser as dparser
from dateutil.relativedelta import relativedelta
from datetime import datetime
from ghost import Time, Ghost
from browser import getDriver
from screener import Screener

ghost = Ghost()
#ghost.wait(Time.SMALL)
#proxy = ghost.getProxy('http://10minutemail.com/')
email = ghost.getEmail()
fullName = ghost.getFullName()
firstName, lastName = fullName.split(' ')
username = ghost.getUsername(fullName)
password = "pantoffelheld"


proxy = ghost.getProxy('http://screener.co/')
ip = proxy[0]
port = proxy[1]

selenium_proxy = "{ip}:{port}".format(ip=ip, port=port)
driver = getDriver(headlessMode=False, proxy=selenium_proxy)

screener = Screener(driver, ghost)
screener.register(firstName, lastName, username, email, password)
#print(relativedelta(datetime.today().strftime('%m-%d-%Y')), )
#print(dparser.parse(row[new_labels['Last Annual Filing']]))
# '.years >= 2:
#     csv = csv.drop(index = index)
#     condition = "Dark since at least 2 years"
#     deleted[-1] = True
