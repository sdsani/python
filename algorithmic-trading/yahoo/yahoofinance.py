import numpy as np
import pandas as pd
import yfinance as yf
from helpers.DataFrameHelper import set_data_frame_options

class YahooFinance:
    def __init__(self, ticker, start, end, sma1, sma2):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.sma1 = sma1
        self.sma2 = sma2
        set_data_frame_options()
        self.stock = yf.download(ticker, start=start, end=end)
        self.build_simple_moving_average()
        self.dualsma = self.build_dual_sma()

    def describe(self):
        print(self.stock)
        self.stock.describe()

    def build_simple_moving_average(self):
        self.stock['SMA1'] = self.stock['Adj Close'].rolling(self.sma1).mean()
        self.stock['SMA2'] = self.stock['Adj Close'].rolling(self.sma2).mean()
        self.stock.dropna(inplace=True)

    def sample_signal(self, sample_type, sample_size):
        if sample_type == 'head':
            return self.dualsma.head(sample_size)
        elif sample_type == 'tail':
            return self.dualsma.tail(sample_size)
        else:
            return self.dualsma.sample(sample_size)

    def build_dual_sma(self):
        dualsma = pd.DataFrame()
        dualsma['change'] = self.stock['Adj Close'].diff()
        dualsma['crossover'] = self.stock['SMA1'] - self.stock['SMA2']
        dualsma['signal'] = np.where(dualsma['crossover'] > 0, 1, -1)
        return dualsma

    def log_stock_column_names(self):
        for col in self.stock.columns:
            print(col)

    def log_dualsma_column_names(self):
        for col in self.dualsma.columns:
            print(col)