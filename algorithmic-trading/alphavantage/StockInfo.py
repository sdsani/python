import numpy as np
import pandas as pd
import pandas_datareader.data as pdr
from datetime import datetime
import matplotlib.pyplot as plt
import requests
import json
from helpers.DataFrameHelper import set_data_frame_options


# https://www.alphavantage.co/
# Premium service will cost you $50/Month

# This class is based on following exercise
# https://colab.research.google.com/drive/1Wevcd45qwNVTKXzQVeOKwrB4Sn_IGjoN#scrollTo=UWuaIbZdvnJh

class StockInfo:
    generic_url = 'https://www.alphavantage.co/query?function={function}&symbol={ticker}&apikey={key}'

    # Free service params
    key = 'SQZSDKNR18C8UYOW'
    column_names = ['open', 'high', 'low', 'close', 'adjusted close', 'volume', 'dividend amount', 'split coefficient']
    function = 'TIME_SERIES_DAILY_ADJUSTED'
    meta_key = 'Time Series (Daily)'

    # Premium service params
    premium_key = 'demo'
    premium_column_names = ['open', 'high', 'low', 'close', 'volume']
    premium_function = 'TIME_SERIES_DAILY'
    premium_meta_key = 'Time Series (Daily)'

    simple_moving_average_1 = 20
    simple_moving_average_2 = 50

    def __init__(self, ticker):
        self.stock_df = None
        self.use_premium = False
        self.ticker = ticker
        set_data_frame_options()
        self.load_data()

    def build_service_url(self, use_premium):
        return self.__class__.generic_url.format(function=self.get_function(use_premium), \
                                                 ticker=self.ticker, \
                                                 key=self.get_key(use_premium))

    def get_key(self, use_premium):
        if use_premium:
            return self.__class__.premium_key
        else:
            return self.__class__.key

    def get_column_names(self, use_premium):
        if use_premium:
            return self.__class__.premium_column_names
        else:
            return self.__class__.column_names

    def get_function(self, use_premium):
        if use_premium:
            return self.__class__.premium_function
        else:
            return self.__class__.function

    def get_meta_key(self, use_premium):
        if use_premium:
            return self.__class__.premium_meta_key
        else:
            return self.__class__.meta_key

    def load_data(self):
        response = requests.get(self.build_service_url(self.use_premium))

        # Service returns response as Json. Transform into dictionary.
        alphadict = json.loads(response.text)
        print(alphadict.keys())

        # print("JSON representation of the data")
        # print(alphadict)
        # print("Get keys in the data")

        # Next only time series data. Here we are ignoring the metadata
        stock = pd.DataFrame(alphadict[self.get_meta_key(self.use_premium)]).T

        # Transform column names from [1. open, 2. high, 3. low, 4. close, 5. volume] to following
        stock.columns = self.get_column_names(self.use_premium)
        # print(type(stock['close'][1]))

        # Data in columns is coming back as strings so following conversion is necessary
        stock = stock.astype(float)
        # print(type(stock['close'][1]))

        # Convert pandas default dataframe index attribute into a datetime index
        # attribute so that you have a standard time series
        stock.index = pd.to_datetime(stock.index)
        self.stock_df = stock
        dual_moving_average = self.build_dual_moving_average()
        # merge stock with dual moving average
        self.stock_df.join(dual_moving_average, how='left').head()

    def sort(self, sort_asc):
        if sort_asc:
            self.stock_df = self.stock_df.sort_index(ascending=True)
        else:
            self.stock_df = self.stock_df.sort_index(ascending=False)

    # def plot(self, column_name):
    #    self.stock_df[column_name].plot(figsize=(20, 5), title=f'{self.ticker} daily closing prices'), plt.show();

    def plot_moving_average(self):
        # 20 days and 50 days simple moving average.
        self.build_dual_moving_average()
        # self.stock_df['SMA1'] = self.build_moving_average('close', self.__class__.simple_moving_average_1)
        # self.stock_df['SMA2'] = self.build_moving_average('close', self.__class__.simple_moving_average_2)
        self.stock_df.dropna(inplace=True)
        # print(self.stock_df)
        self.stock_df[['close', 'SMA1', 'SMA2']].plot(figsize=(20, 5), grid=True,
                                                      title=f'The 20 and 50 day simple moving averages of {self.ticker}') \
                                                      , plt.show();

    def build_moving_average(self, column_name, number_of_days):
        return self.stock_df[column_name].rolling(number_of_days).mean()

    def build_dual_moving_average(self):
        # Start with empty dataframe
        dual_moving_average = pd.DataFrame()
        # 20 days and 50 days simple moving average.
        dual_moving_average['SMA1'] = self.build_moving_average('close', self.__class__.simple_moving_average_1)
        dual_moving_average['SMA2'] = self.build_moving_average('close', self.__class__.simple_moving_average_2)
        dual_moving_average['change'] = self.stock_df['close'].diff()
        dual_moving_average['crossover'] = dual_moving_average['SMA1'] - dual_moving_average['SMA2']
        # When 20 days SMA is above 50 days SMA then signal is +ve and vice versa
        dual_moving_average['signal'] = np.where(dual_moving_average['crossover'] > 0, 1, -1)
        dual_moving_average.dropna(inplace=True)
        dual_moving_average = dual_moving_average.sort_index(ascending=True)
        print(dual_moving_average.tail(20))
        return dual_moving_average

    def sample(self, sample_size):
        # Picks a random sample from the dataset in your dataframe
        print(self.stock_df.sample(10))

    def head(self):
        # Picks a random sample from the dataset in your dataframe
        print(self.stock_df.head())

    def tail(self):
        # Picks a random sample from the dataset in your dataframe
        print(self.stock_df.tail())
