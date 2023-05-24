from datetime import datetime
from financialservices.yahoo.yahoofinance import YahooFinance

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

start = datetime(2018, 1, 1)
end = datetime(2023, 5, 23)

tickers = ['GTLB', 'RIVN', 'TSLA', 'MSFT', 'AAPL']
for ticker in tickers:
    y_finance = YahooFinance(ticker, start, end, 20, 50)
    y_finance.log_stock_column_names()
    print(f"Signal info for {ticker}")
    print(y_finance.sample_signal('tail', 20))

# https://pandas.pydata.org/docs/getting_started/intro_tutorials/04_plotting.html#
# https://pandas.pydata.org/docs/user_guide/visualization.html#visualization-other
#y_finance.get_history()['Close'].plot.area()
#y_finance.get_history().plot.area()
#plt.show()

