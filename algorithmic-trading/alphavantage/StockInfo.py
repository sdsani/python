import numpy as np
import pandas as pd
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

    def __init__(self, ticker, simple_moving_average_1, simple_moving_average_2):
        self.stock_df = None
        self.signal_df = None
        self.use_premium = False
        self.ticker = ticker
        self.simple_moving_average_1 = simple_moving_average_1
        self.simple_moving_average_2 = simple_moving_average_2
        set_data_frame_options()
        self.load_data()
        self.build_signal()

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
        #print(alphadict.keys())

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
        self.stock_df = self.stock_df.sort_index(ascending=True)

    # def plot(self, column_name):
    #    self.stock_df[column_name].plot(figsize=(20, 5), title=f'{self.ticker} daily closing prices'), plt.show();

    def plot_moving_average(self):
        self.signal_df[['close', 'SMA1', 'SMA2']].plot(figsize=(20, 5), grid=True,
                                                      title=f'The 20 and 50 day simple moving averages of {self.ticker}'), plt.show();

    def build_moving_average(self, column_name, number_of_days):
        return self.stock_df[column_name].rolling(number_of_days).mean()

    def build_signal(self):
        # Start with empty dataframe
        self.signal_df = pd.DataFrame()
        # 20 days and 50 days simple moving average.
        self.signal_df['SMA1'] = self.build_moving_average('close', self.simple_moving_average_1)
        self.signal_df['SMA2'] = self.build_moving_average('close', self.simple_moving_average_2)
        self.signal_df['change'] = self.stock_df['close'].diff()
        self.signal_df['crossover'] = self.signal_df['SMA1'] - self.signal_df['SMA2']
        self.signal_df['close'] = self.stock_df['close']
        # When 20 days SMA is above 50 days SMA then signal is +ve and vice versa
        self.signal_df['signal'] = np.where(self.signal_df['crossover'] > 0, 1, -1)
        self.signal_df.dropna(inplace=True)
        self.signal_df = self.signal_df.sort_index(ascending=True)

    def sample_signal(self, sample_type, sample_size):
        if sample_type == 'head':
            return self.signal_df.head(sample_size)
        elif sample_type == 'tail':
            return self.signal_df.tail(sample_size)
        else:
            return self.signal_df.sample(sample_size)
