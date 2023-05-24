import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import json
import requests
from alphavantage.StockInfo import StockInfo

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

plt.style.use('seaborn')
start = datetime(2020, 1, 1)
end = datetime(2023, 5, 1)


def display_data():
    response = requests.get(
        "https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=EUR&to_symbol=USD&apikey=demo")
    alphadict = json.loads(response.text)
    print(alphadict)
    eur = pd.DataFrame(alphadict['Time Series FX (Daily)']).T
    eur.index = pd.to_datetime(eur.index)
    eur = eur.sort_index(ascending=True)
    eur.columns = ['open', 'high', 'low', 'close']
    eur = eur.astype(float)
    eur.head()
    eur['close'].plot(figsize=(20, 5), title='EUR/USD closing prices'), plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    stocks = ['GTLB', 'RIVN', 'TSLA', 'MSFT', 'AAPL']
    for stock in stocks:
        print(f"Signal info for {stock}")
        av = StockInfo(stock, 20, 50)
        print(av.sample_signal('tail', 20))

    #av = StockInfo('MSFT', 20, 50)
    #print(av.sample_signal('tail', 20))
    #av.plot_moving_average()

    # display_data()
    # av = StockInfo('RIVN')
    #av = StockInfo('MSFT')
    # av = StockInfo('AAPL')
    #av.sort(True)
    #print("Random Sample")
    #av.sample(10)
    #print("Head")
    #av.head()
    #print("Trail")
    #av.tail()
    #av.plot_moving_average()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
