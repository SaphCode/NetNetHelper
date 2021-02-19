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

        self.column_labels = ['Symbol', 'Company Name', 'Cash and Equiv.-most recent quarter',
                                'Assets, current-most recent quarter', 'Liabilities, current-most recent quarter',
                                'Inventory-most recent quarter', 'Receivables-most recent quarter',
                                'Assets, total-most recent quarter', 'Book value (tangible) in dollars-most recent quarter',
                                 'Liabilities, total-most recent quarter', 'Shareholder Equity-most recent quarter',
                                 'Market capitalization', 'Exchange Rate From Price to Financial Reporting Currency',
                                 'Exchange Rate From Financial Reporting Currency to USD', 'Net Income Before Taxes(A)',
                                 'Net Income Before Taxes(A-1)', 'Net Income Before Taxes(A-2)',
                                 'Net Income Before Taxes(A-3)', 'Net Income Before Taxes(A-4)',
                                 'Net Income Before Taxes(A-5)', 'Net Income Before Taxes(A-6)',
                                 'Net Income Before Taxes(A-7)', 'Net Income Before Taxes(A-8)',
                                 'Net Income Before Taxes(A-9)',
                                 ]

        self.new_labels = {
            'Symbol':'Symbol',
            'Company Name':'Company Name',
            'Market/NCAV':'Market/NCAV',
            'NCAV':'NCAV',
            'Market Cap':'Market Cap',
            'AVG 10y EBT':'AVG 10y EBT',
            'Total Assets':'Total Assets',
            'Total Liabilities':'Total Liabilities',
            'Cash & Equivalents':'Cash & Equivalents',
            'Receivables':'Receivables',
            'Inventory':'Inventory',
            '10y Earnings Yield':'10y Earnings Yield',
            'Earnings Trend':'Earnings Trend',
            '3y AVG EBT':'3y AVG EBT',
            'Median EBT 5y':'Median EBT 5y',
            'EBT A-5':'EBT A-5',
            'EBT A-6':'EBT A-6',
            'EBT A-7':'EBT A-7',
            'EBT A-8':'EBT A-8',
            'EBT A-9':'EBT A-9',
            'Median EBT 10y':'Median EBT 10y',
            'Last Annual Filing':'Last Annual Filing',
        }

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
            df.to_csv(master_csv_path)
        master = pd.read_csv('{}/{}'.format(self.working_directory, 'master.csv'))#
        print(master.columns)
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
        new_labels = self.new_labels
        out_filepath = '{parent}/{file}'.format(parent = self.working_directory, file = 'out.csv')
        keys = ['Symbol', 'Company Name']
        if not os.path.exists(out_filepath):
            #create empty out.csv
            self.logger.info("Creating empty outfile .. (out.csv)")
            df = pd.DataFrame(columns = keys)
            df.to_csv(out_filepath)
        out = pd.read_csv('{parent}/{file}'.format(parent = self.working_directory, file = 'out.csv'))
        master = pd.DataFrame(columns = self.new_labels)
        master[new_labels['Symbol']] = out['Symbol']
        master[new_labels['Company Name']] = out['Company Name']
        master[new_labels['Market Cap']] = out['Market capitalization']*out['Exchange Rate From Price to Financial Reporting Currency']*out['Exchange Rate From Financial Reporting Currency to USD']
        master[new_labels['Cash & Equivalents']] = out['Cash and Equiv.-most recent quarter']*out['Exchange Rate From Financial Reporting Currency to USD']
        master[new_labels['Receivables']] = out['Receivables-most recent quarter']*out['Exchange Rate From Financial Reporting Currency to USD']
        master[new_labels['Inventory']] = out['Inventory-most recent quarter']*out['Exchange Rate From Financial Reporting Currency to USD']
        master[new_labels['Total Liabilities']] = out['Liabilities, total-most recent quarter']*out['Exchange Rate From Financial Reporting Currency to USD']
        master[new_labels['NCAV']] = master[new_labels['Cash & Equivalents']] + 0.75 * master[new_labels['Receivables']] + 0.5 * master[new_labels['Inventory']] - master[new_labels['Total Liabilities']]
        master[new_labels['Market/NCAV']] = master['Market Cap']/master[new_labels['NCAV']]
        master[new_labels['AVG 10y EBT']] = out[['Net Income Before Taxes(A)', 'Net Income Before Taxes(A-1)', 'Net Income Before Taxes(A-2)',
                                            'Net Income Before Taxes(A-3)', 'Net Income Before Taxes(A-4)', 'Net Income Before Taxes(A-5)',
                                            'Net Income Before Taxes(A-6)', 'Net Income Before Taxes(A-7)', 'Net Income Before Taxes(A-8)',
                                            'Net Income Before Taxes(A-9)']].mean(axis = 1, skipna = True) * out['Exchange Rate From Financial Reporting Currency to USD']
        master[new_labels['Total Assets']] = out['Assets, total-most recent quarter']*out['Exchange Rate From Financial Reporting Currency to USD']
        master[new_labels['10y Earnings Yield']] = master[new_labels['AVG 10y EBT']]/master[new_labels['Market Cap']]
        master[new_labels['3y AVG EBT']] = out[['Net Income Before Taxes(A)', 'Net Income Before Taxes(A-1)', 'Net Income Before Taxes(A-2)']].mean(axis = 1, skipna=True)
        master[new_labels['Earnings Trend']] = (1 - (master[new_labels['3y AVG EBT']]/master[new_labels['AVG 10y EBT']]))*-1
        master[new_labels['Median EBT 5y']] = out[['Net Income Before Taxes(A)', 'Net Income Before Taxes(A-1)',
                                            'Net Income Before Taxes(A-2)', 'Net Income Before Taxes(A-3)',
                                            'Net Income Before Taxes(A-4)']].median(axis = 1, skipna = True) * out['Exchange Rate From Financial Reporting Currency to USD']
        master[new_labels['EBT A-5']] = out['Net Income Before Taxes(A-5)'] * out['Exchange Rate From Financial Reporting Currency to USD']
        master[new_labels['EBT A-6']] = out['Net Income Before Taxes(A-6)'] * out['Exchange Rate From Financial Reporting Currency to USD']
        master[new_labels['EBT A-7']] = out['Net Income Before Taxes(A-7)'] * out['Exchange Rate From Financial Reporting Currency to USD']
        master[new_labels['EBT A-8']] = out['Net Income Before Taxes(A-8)'] * out['Exchange Rate From Financial Reporting Currency to USD']
        master[new_labels['EBT A-9']] = out['Net Income Before Taxes(A-9)'] * out['Exchange Rate From Financial Reporting Currency to USD']
        master[new_labels['Median EBT 10y']] = out[['Net Income Before Taxes(A)', 'Net Income Before Taxes(A-1)', 'Net Income Before Taxes(A-2)',
                                             'Net Income Before Taxes(A-3)', 'Net Income Before Taxes(A-4)', 'Net Income Before Taxes(A-5)',
                                             'Net Income Before Taxes(A-6)', 'Net Income Before Taxes(A-7)', 'Net Income Before Taxes(A-8)',
                                             'Net Income Before Taxes(A-9)']].median(axis = 1, skipna = True)
        master[new_labels['Last Annual Filing']] = out['Last Annual Filing']
        #master.to_csv('{parent}/{filename}'.format(parent = self.working_directory, filename = 'test.csv'))
        master = master.set_index([new_labels['Symbol'], new_labels['Company Name']])

        xl = pd.ExcelFile(r'{wd}/{file}'.format(wd = self.working_directory, file = 'TOP_SECRET.xlsx'))
        dfs = {sheet: xl.parse(sheet) for sheet in xl.sheet_names}
        nopelist = dfs['Nopelist'].set_index(keys)
        not_sure_list = dfs['Not Sure List'].set_index(keys)
        not_possible_list = dfs['Not possible List']

        for index in master.index:
            # self.logger.debug('Checking index: {}'.format(index))
            if index in nopelist.index:
                self.logger.info('Dropping index: {} because it is in Nopelist'.format(index))
                master.drop(index, inplace=True)
                continue
            if index in not_sure_list.index:
                self.logger.info('Dropping index: {} because it is in Not Sure List.'.format(index))
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

        master = self.get_sorted_master(master)
        master.to_csv('{parent}/{filename}'.format(parent = self.working_directory, filename = 'netnets.csv'))


    def get_sorted_master(self, csv):
        reduced_df = self.drop_unpromising(csv)
        reduced_df['Score'] = self.calculate_score(reduced_df)
        sorted_df = reduced_df.sort_values(by=['Score'], ascending = False)
        self.logger.info('Sorted data by score.')
        return sorted_df


    def drop_unpromising(self, csv):
        new_labels = self.new_labels
        score = 0
        deleted = []
        nrows = len(csv.index)
        for index, row in csv.iterrows():
            condition = ''
            deleted.append(False)
            if row[new_labels['AVG 10y EBT']] <= 0:
                csv = csv.drop(index = index)
                condition = 'Loss on AVG in last 10y'
                deleted[-1] = True
            #wenn earnings yield größer als 1000%
            elif ( row[new_labels['3y AVG EBT']] / row[new_labels['Market Cap']] ) > 10:
                csv = csv.drop(index = index)
                condition = "Earnings Yield > 1000%"
                deleted[-1] = True
            #wenn inventory mehr als 85% von ncav ist
            elif (row[new_labels['NCAV']] + row[new_labels['Total Liabilities']])* 0.85 <= row[new_labels['Inventory']]:
                csv = csv.drop(index = index)
                condition = "Inventory > 85%"
                deleted[-1] = True
            #wenn receivables mehr als 85% von ncav ist
            elif (row[new_labels['NCAV']] + row[new_labels['Total Liabilities']]) * 0.95 <= row[new_labels['Receivables']]:
                csv = csv.drop(index = index)
                condition = "Receivables > 95%"
                deleted[-1] = True
            #wenn die earnings unreasonable nach oben gegangen sind
            elif row[new_labels['3y AVG EBT']] > (row[new_labels['AVG 10y EBT']] * 15):
                csv = csv.drop(index = index)
                condition = "Earnings Trend is death"
                deleted[-1] = True
            elif row[new_labels['Median EBT 5y']] <= 0:
                csv = csv.drop(index = index)
                condition = "3 of 5 years negative earnings"
                deleted[-1] = True
            elif relativedelta(datetime.today(), dparser.parse(row[new_labels['Last Annual Filing']])).years >= 2:
                csv = csv.drop(index = index)
                condition = "Dark since at least 2 years"
                deleted[-1] = True
            if deleted[-1] == True:
                self.logger.info('Deleted {index}, because {condition}'.format(index = index, condition = condition))
            '''
            #wenns kein netnet ist, warum auch immer
            elif row[new_labels['NCAV']] < row[new_labels['Market Cap']]:
                csv = csv.drop(index = index)
                condition = "ALARM DIESE CONDITION SOLLTE NICHT AUFTRETEN GROSSER ALARM ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
            '''
        self.logger.info('Deleted {sum} ({percentage}%) companies.'.format(sum = sum(deleted), percentage = int(round(sum(deleted)*100/nrows, 0))))
        return csv


    def calculate_score(self, df):
        new_labels = self.new_labels
        self.logger.info('Calculating score.')
        score = 1-df[new_labels['Market/NCAV']]
        score += df[new_labels['10y Earnings Yield']]
        score += df[new_labels['Cash & Equivalents']]/df[new_labels['NCAV']]
        score += (df[new_labels['NCAV']] + df[new_labels['Total Liabilities']])/df[new_labels['Total Assets']]
        self.logger.info('Calculated score.')
        return score
