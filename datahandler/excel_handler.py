import os
import logging
import shutil
import pandas as pd
import time
from random import randint
import copy
import numpy as np
import statistics
import dateutil.parser as dparser
from dateutil.relativedelta import relativedelta
from datetime import datetime
from scraper.stockprice import *
from .labels import Labels

class ExcelHandler:

    def __init__(self, working_directory):
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(pathname)s - %(lineno)d: %(message)s')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        logger_fh = logging.FileHandler('log/lexcel_handler.log')
        logger_fh.setLevel(logging.WARNING)
        logger_fh.setFormatter(formatter)

        logger_ch = logging.StreamHandler()
        logger_ch.setLevel(logging.DEBUG)
        logger_ch.setFormatter(formatter)

        self.logger.addHandler(logger_fh)
        self.logger.addHandler(logger_ch)

        if os.path.exists(working_directory):
            self.working_directory = working_directory
        else:
            logging.error('Directory {} does not exist.'.format(working_directory))
            raise Exception('Directory {} does not exist.'.format(working_directory))

        self.main_csv = self.working_directory + '/' + 'NetNets.csv'

    def locate_excel(self):
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        path = self.__get_path(downloads_guid)
        self.logger.info('Found path: {}'.format(path))
        files = [filename for filename in os.listdir(path) if (filename.startswith('data') and filename.endswith('.csv'))]
        self.logger.info('Found files:\n {}'.format(files))

        return path, files

    def move_to_wd(self, parent_directory, files):
        destination = self.working_directory
        for file in files:
            self.logger.debug('Moving file {} from {} to {}'.format(file, parent_directory, destination))
            current_path = parent_directory + '/' + file
            destination_path = destination + '/' + file
            shutil.move(current_path, destination_path)
        self.logger.info('Moved all files successfully.')

    def join_data(self):
        self.logger.info('Deleting output from previous run ..')
        keys = ['Symbol', 'Company Name']

        out_csv_path = '{parent}/{file}'.format(parent = self.working_directory, file = 'out.csv')
        if os.path.exists(out_csv_path):
            os.remove(out_csv_path)

        master_csv_path = '{parent}/{file}'.format(parent = self.working_directory, file = 'master.csv')
        if not os.path.exists(master_csv_path):
            self.logger.info("Creating a master.csv file")
            df = pd.DataFrame(columns = keys)
            df.to_csv(master_csv_path, index=False)
        master = pd.read_csv('{}/{}'.format(self.working_directory, 'master.csv'))#
        master.set_index(keys, inplace = True)
        #print(keys in master.columns)

        csvs = [file for file in os.listdir(self.working_directory) if file.startswith('data') and file.endswith('.csv')]
        for csv in csvs:
            df = pd.read_csv('{}/{}'.format(self.working_directory, csv))
            master = master.append(df[keys]).drop_duplicates(subset = keys)
        out = master.copy()

        master.to_csv('{}/{}'.format(self.working_directory, 'master.csv'), index = False) ##TODO: master file should keep screened companies

        for csv in csvs:
            df = pd.read_csv('{}/{}'.format(self.working_directory, csv))
            out = out.merge(df, on = keys, how = 'outer')
            for col in out.columns:
                if col.endswith('_x'):
                    out[col].fillna(out[col.replace('_x', '_y')], inplace = True)
                    out[col.replace('_x', '')] = out[col]
                if col.endswith('_x') or col.endswith('_y'):
                    del out[col]

        for csv in csvs:
            os.remove('{parent}/{file}'.format(parent = self.working_directory, file = csv))

        out.dropna(axis = 0, how = 'all', inplace = True)
        out.to_csv('{}/{}'.format(self.working_directory, 'out.csv'), index = False)


    def __clean_up(self, df):
        for col_x in df.columns:
            for col_y in df.columns:
                if col_x.endswith('_x') and col_y.endswith('_y'):
                    if col_x.replace('_x', '') == col_y.replace('_y', ''):
                        #print('{x}, {y}'.format(x=col_x, y=col_y))
                        #df2 = pd.DataFrame({'x': df[col_x], 'y': df[col_y]})
                        #print(df2)
                        if df[col_x].isnull().all():
                            df[col_x.replace('_x', '')] = df[col_y]
                        elif df[col_y].isnull().all():
                            df[col_y.replace('_y', '')] = df[col_x]
        #df.to_csv('{}/{}{}'.format(self.working_directory, randint(0, 10000), 'test.csv'))
        for col in df.columns:
            if col.endswith('_x') or col.endswith('_y'):
                del df[col]

        return df


    def __get_path(self, guid):
        """Returns the default folder, identified by guid, path for linux or windows"""
        self.logger.debug('Searching folder with guid: {}'.format(guid))
        if os.name == 'nt':
            import winreg
            sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                location = winreg.QueryValueEx(key, guid)[0]
            return location
        else:
            return os.path.join(os.path.expanduser('~'), 'Downloads')


    def get_master_sheet(self):
        out_filepath = '{parent}/{file}'.format(parent = self.working_directory, file = 'out.csv')
        keys = ['Symbol', 'Company Name']
        if not os.path.exists(out_filepath):
            #create empty out.csv
            self.logger.info("Creating empty outfile .. (out.csv)")
            df = pd.DataFrame(columns = keys)
            df.to_csv(out_filepath)
        out = pd.read_csv('{parent}/{file}'.format(parent = self.working_directory, file = 'out.csv'))
        master = pd.DataFrame()
        master[Labels.symbol] = out['Symbol']
        master[Labels.name] = out['Company Name']
        master[Labels.mcap] = out['Market capitalization']*out['Exchange Rate From Price to Financial Reporting Currency']*out['Exchange Rate From Financial Reporting Currency to USD']
        master[Labels.cash] = out['Cash and Equiv.-most recent quarter']*out['Exchange Rate From Financial Reporting Currency to USD']
        master[Labels.receivables] = out['Receivables-most recent quarter']*out['Exchange Rate From Financial Reporting Currency to USD']
        master[Labels.inventory] = out['Inventory-most recent quarter']*out['Exchange Rate From Financial Reporting Currency to USD']
        master[Labels.total_liabilities] = out['Liabilities, total-most recent quarter']*out['Exchange Rate From Financial Reporting Currency to USD']
        master[Labels.ncav] = master[Labels.cash] + 0.75 * master[Labels.receivables] + 0.5 * master[Labels.inventory] - master[Labels.total_liabilities]
        master[Labels.mcap_to_ncav] = master[Labels.mcap]/master[Labels.ncav]
        master[Labels.avg_10y_ebt] = out[['Net Income Before Taxes(A)', 'Net Income Before Taxes(A-1)', 'Net Income Before Taxes(A-2)',
                                            'Net Income Before Taxes(A-3)', 'Net Income Before Taxes(A-4)', 'Net Income Before Taxes(A-5)',
                                            'Net Income Before Taxes(A-6)', 'Net Income Before Taxes(A-7)', 'Net Income Before Taxes(A-8)',
                                            'Net Income Before Taxes(A-9)']].mean(axis = 1, skipna = True) * out['Exchange Rate From Financial Reporting Currency to USD']
        master[Labels.total_assets] = out['Assets, total-most recent quarter']*out['Exchange Rate From Financial Reporting Currency to USD']
        master[Labels.earnings_yield_10y] = master[Labels.avg_10y_ebt]/master[Labels.mcap]
        master[Labels.avg_3y_ebt] = out[['Net Income Before Taxes(A)', 'Net Income Before Taxes(A-1)', 'Net Income Before Taxes(A-2)']].mean(axis = 1, skipna=True)
        master[Labels.med_5y_ebt] = out[['Net Income Before Taxes(A)', 'Net Income Before Taxes(A-1)',
                                            'Net Income Before Taxes(A-2)', 'Net Income Before Taxes(A-3)',
                                            'Net Income Before Taxes(A-4)']].median(axis = 1, skipna = True) * out['Exchange Rate From Financial Reporting Currency to USD']
        master[Labels.ebt_m5] = out['Net Income Before Taxes(A-5)'] * out['Exchange Rate From Financial Reporting Currency to USD']
        master[Labels.ebt_m6] = out['Net Income Before Taxes(A-6)'] * out['Exchange Rate From Financial Reporting Currency to USD']
        master[Labels.ebt_m7] = out['Net Income Before Taxes(A-7)'] * out['Exchange Rate From Financial Reporting Currency to USD']
        master[Labels.ebt_m8] = out['Net Income Before Taxes(A-8)'] * out['Exchange Rate From Financial Reporting Currency to USD']
        master[Labels.ebt_m9] = out['Net Income Before Taxes(A-9)'] * out['Exchange Rate From Financial Reporting Currency to USD']
        master[Labels.med_10y_ebt] = out[['Net Income Before Taxes(A)', 'Net Income Before Taxes(A-1)', 'Net Income Before Taxes(A-2)',
                                             'Net Income Before Taxes(A-3)', 'Net Income Before Taxes(A-4)', 'Net Income Before Taxes(A-5)',
                                             'Net Income Before Taxes(A-6)', 'Net Income Before Taxes(A-7)', 'Net Income Before Taxes(A-8)',
                                             'Net Income Before Taxes(A-9)']].median(axis = 1, skipna = True)
        master[Labels.last_annual_date] = out['Last Annual Filing']
        #master.to_csv('{parent}/{filename}'.format(parent = self.working_directory, filename = 'test.csv'))
        master = master.set_index([Labels.symbol, Labels.name])

        xl = pd.ExcelFile(r'{wd}/{file}'.format(wd = self.working_directory, file = 'TOP_SECRET.xlsx'))
        dfs = {sheet: xl.parse(sheet) for sheet in xl.sheet_names}
        nopelist = dfs['Nopelist'].set_index(keys)
        too_complicated_df = dfs['Too Complicated'].set_index(keys)
        not_possible_list = dfs['Not possible List']
        too_expensive_df = dfs['Too Expensive'].set_index(keys) # TODO: new, test this
        portfolio_df = dfs['Portfolio'].set_index(keys) # TODO: new, test this
        intrinsic_df = dfs['Intrinsic Value'].set_index(keys)
        for index in master.index:
            # self.logger.debug('Checking index: {}'.format(index))
            if index in nopelist.index:
                self.logger.info('Dropping index: {} because it is in Nopelist'.format(index))
                master.drop(index, inplace=True)
                continue
            if index in too_complicated_df.index:
                self.logger.info('Dropping index: {} because it is in Too Complicated.'.format(index))
                master.drop(index, inplace=True)
                continue
            if index in too_expensive_df.index:
                row = too_expensive_df.loc[index]
                expiry_year = datetime.strptime("3000", "%Y")
                if not row['expires'].isna().any():
                    expiry_year = datetime.strptime(str(int(row['expires'][0])), '%Y')
                today = datetime.today()
                if (expiry_year > today):
                    self.logger.info('Dropping index: {} because it is in Too Expensive.'.format(index))
                    master.drop(index, inplace=True)
                    continue
                else:
                    mcap_then = row['mcap at day of entry']
                    mcap_now = row['current mcap']
                    if mcap_now.isna().any():
                        yfinance_ticker = convert_to_yticker(index[0])
                        mcap_now = getPrice(yfinance_ticker, datetime.today())
                    if (mcap_then * 0.8 >= mcap_now): # has NOT dropped by 20%
                        self.logger.info('Dropping index: {} because it is in Too Expensive.'.format(index))
                        master.drop(index, inplace=True)
                        continue
            if index in portfolio_df.index:
                self.logger.info('Dropping index: {} because it is in Portfolio.'.format(index))
                master.drop(index, inplace=True)
                continue
            if index in intrinsic_df.index:
                self.logger.info('Dropping index: {} because it is in Intrinsic Value.'.format(index))
                master.drop(index, inplace=True)
                continue


            deleted = False
            for exchange in not_possible_list['Exchange']:
                if not deleted:
                    if isinstance(index[0], str):
                        if exchange == index[0].split(':')[0]:
                            self.logger.info('Dropping index: {} because we cant buy it.'.format(index))
                            master.drop(index, inplace=True)
                            deleted = True

        return master
