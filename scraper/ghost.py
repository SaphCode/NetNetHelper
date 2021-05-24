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


    def wait(self, approx_time):
        if (approx_time - 5 * self.large_sigma):
            wait_time = gauss(approx_time, self.large_sigma)
        elif (approx_time - 5 * self.med_sigma):
            wait_time = gauss(approx_time, self.med_sigma)
        if (approx_time - 5 * self.small_sigma):
            wait_time = gauss(approx_time, self.small_sigma)

        self.logger.debug('Waiting {} seconds for page to load'.format(round(wait_time)))
        sleep(wait_time)
