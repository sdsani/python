from helpers.DataFrameHelper import set_data_frame_options
import abc
import pandas as pd
import numpy as np

class FinanceService:

    __metaclass__ = abc.ABCMeta

    def __init__(self, ticker, closing_column_name, sma1, sma2):
        self.stock_data = None
        self.signal_data = None
        self.ticker = ticker
        self.closing_column_name = closing_column_name
        self.sma1 = sma1
        self.sma2 = sma2
        set_data_frame_options()
        self.load_financial_data()

    @abc.abstractmethod
    def load_financial_data(self):
        """Abstract method to be implemented by implemented class"""

    def describe(self):
        print(self.stock_data)
        self.stock_data.describe()

    def build_simple_moving_average(self):
        # print(self.stock_data)
        print(f"{self.sma1}, {self.sma2}")
        self.stock_data['SMA1'] = self.stock_data[self.closing_column_name].rolling(self.sma1).mean()
        self.stock_data['SMA2'] = self.stock_data[self.closing_column_name].rolling(self.sma2).mean()
        self.stock_data.dropna(inplace=True)

    def build_dual_signal_data(self):
        self.signal_data = pd.DataFrame()
        self.signal_data['change'] = self.stock_data[self.closing_column_name].diff()
        self.signal_data['crossover'] = self.stock_data['SMA1'] - self.stock_data['SMA2']
        self.signal_data['signal'] = np.where(self.signal_data['crossover'] > 0, 1, -1)

    def sample_signal(self, sample_type, sample_size):
        if sample_type == 'head':
            return self.signal_data.head(sample_size)
        elif sample_type == 'tail':
            return self.signal_data.tail(sample_size)
        else:
            return self.signal_data.sample(sample_size)

    def log_stock_column_names(self):
        for col in self.stock_data.columns:
            print(col)

    def log_signal_data_column_names(self):
        for col in self.signal_data.columns:
            print(col)

