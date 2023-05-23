from datetime import datetime
import matplotlib.pyplot as plt
from oop.yahoofinance import YahooFinance
import pandas as pd
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

start = datetime(2023, 1, 1)
end = datetime(2023, 5, 1)

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 1000)

#tickers = ['AAPL', 'MSFT', 'AMANX', 'AMAGX']
#y_finance = YahooFinance('AMANX', start, end)
#y_finance = YahooFinance('AAPL', start, end)
y_finance = YahooFinance('MSFT', start, end)
#print(y_finance.get_head())
#print(y_finance.get_tail())
print(len(y_finance.get_history().index))
print(y_finance.get_history())

# https://pandas.pydata.org/docs/getting_started/intro_tutorials/04_plotting.html#
# https://pandas.pydata.org/docs/user_guide/visualization.html#visualization-other
#y_finance.get_history()['Close'].plot.area()
y_finance.get_history().plot.area()
plt.show()

