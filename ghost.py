from enum import IntEnum
class Time(IntEnum):
    VERY_SMALL = 1
    SMALL = 2
    MEDIUM = 3
    LONG = 6
    VERY_LONG = 20

from time import sleep
from random import gauss, randint
import logging
from proxyscrape import create_collector
import names
from selenium import webdriver
from sys import platform
from browser import getDriver
import urllib.request , socket
class Ghost:
    def __init__(self):
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(pathname)s - %(lineno)d: %(message)s')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        logger_fh = logging.FileHandler('log/ghost.log')
        logger_fh.setLevel(logging.WARNING)
        logger_fh.setFormatter(formatter)

        logger_ch = logging.StreamHandler()
        logger_ch.setLevel(logging.DEBUG)
        logger_ch.setFormatter(formatter)

        self.logger.addHandler(logger_fh)
        self.logger.addHandler(logger_ch)

        self.small_sigma = 0.1
        self.med_sigma = 3
        self.large_sigma = 10

        self.working_proxies = []

        self.collector = create_collector('proxies', 'http')

    def wait(self, approx_time):
        if (approx_time - 5 * self.large_sigma):
            wait_time = gauss(approx_time, self.large_sigma)
        elif (approx_time - 5 * self.med_sigma):
            wait_time = gauss(approx_time, self.med_sigma)
        if (approx_time - 5 * self.small_sigma):
            wait_time = gauss(approx_time, self.small_sigma)

        self.logger.debug('Waiting {} seconds for page to load'.format(round(wait_time)))
        sleep(wait_time)

    def getProxy(self, site):
        badProxy = True
        proxy = ''

        while (badProxy):
            proxy_o = self.collector.get_proxy()
            proxy = "{ip}:{port}".format(ip=proxy_o[0], port=proxy_o[1])
            badProxy = self.is_bad_proxy(proxy, site)

        self.logger.info('Proxy: {} acquired.'.format(proxy))
        return proxy

    def getFullName(self):
        full_name = names.get_full_name()
        self.logger.info('Full Name: {} acquired.'.format(full_name))
        return full_name

    def getUsername(self, fullName):
        firstName, lastName = fullName.split(' ')
        lf = len(firstName)
        ll = len(lastName)
        lf_i = randint(1, lf)
        ll_i = randint(1, ll)
        userf = firstName[:lf_i]
        userl = lastName[:ll_i]
        num = randint(101,1000)
        username = userf + userl + str(num)
        self.logger.info('Generated username {us} from {fn}'.format(us = username, fn = fullName))
        return username

    # def checkProxies(proxyList):
    #     socket.setdefaulttimeout(180)
    #     for item in proxyList:
    #         if is_bad_proxy(item):
    #             self.logger.debug("Bad Proxy", item)
    #         else:
    #             self.logger.debug(item, "is working")
    #             self.working_proxies.append(item)

    def getEmail(self):
        # email = input("Please enter email here. Get it from 10minutemail or something. ENTER EMAIL:\n")
        # if "@" not in email:
        #     print("Not a valid email.")
        #     email = self.getEmail()
        # return email
        minute_mail = 'http://10minutemail.com/'
        proxy = self.getProxy(minute_mail)

        ip = proxy[0]
        port = proxy[1]

        selenium_proxy = "{ip}:{port}".format(ip=ip, port=port)
        self.email_driver = getDriver(headlessMode=False, proxy=selenium_proxy)
        self.email_driver.get(minute_mail)
        self.wait(Time.MEDIUM)
        accept_btn = '/html/body/div[1]/div/div[1]/div/button[2]'
        try:
            self.email_driver.find_element_by_xpath(accept_btn).click()
        except Exception as e:
            self.logger.error(str(e))
        self.wait(Time.SMALL)
        self.email = self.email_driver.find_element_by_xpath('/html/body/div[1]/div/section[1]/div/div[1]/div[2]/input').get_attribute('value')
        return self.email


    def is_bad_proxy(self, pip, site):
        try:
            self.logger.debug('Testing proxy: {} on site: {}'.format(pip, site))
            proxy_handler = urllib.request.ProxyHandler({'http': pip})
            opener = urllib.request.build_opener(proxy_handler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            sock=urllib.request.urlopen(site)  # change the url address here
            #sock=urllib.urlopen(req)
        except urllib.error.HTTPError as e:
            self.logger.error('Error code: ', e.code)
            return e.code
        except Exception as detail:
            self.logger.error( "ERROR:", detail)
            return 1
        return 0


    def getMailbox(self, email):
        if not self.email_driver:
            raise Exception('Driver is already closed. cannot retrieve messages')
        self.email_driver.find_element_by_xpath('/html/body/div[1]/div/section[2]/div/div/div[1]').click()
