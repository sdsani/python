import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
from financialservices.financeservice import FinanceService


# https://www.alphavantage.co/
# Premium service will cost you $50/Month

# This class is based on following exercise
# https://colab.research.google.com/drive/1Wevcd45qwNVTKXzQVeOKwrB4Sn_IGjoN#scrollTo=UWuaIbZdvnJh

class StockInfo(FinanceService):
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
        self.use_premium = False
        FinanceService.__init__(self, ticker, 'close', simple_moving_average_1, simple_moving_average_2)

    def load_financial_data(self):
        self.load_data()
        self.build_simple_moving_average()
        self.build_dual_signal_data()

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
        self.stock_data = stock
        self.stock_data = self.stock_data.sort_index(ascending=True)

    def plot_moving_average(self):
        self.signal_data[['close', 'SMA1', 'SMA2']].plot(figsize=(20, 5), grid=True,
                                                      title=f'The 20 and 50 day simple moving averages of {self.ticker}'), plt.show();
