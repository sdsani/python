import pandas as pd
import pandas_datareader.data as pdr
from datetime import datetime
import matplotlib.pyplot as plt
import json
import requests

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

plt.style.use('seaborn')
start = datetime(2020, 1, 1)
end = datetime(2023, 5, 1)

def display_data():
    #inflation = pdr.DataReader('T5YIE', 'fred', start, end)
    inflation = pdr.DataReader('THREEFY5', 'fred', start, end)
    inflation.plot(figsize=(20, 5), title='5 year forward inflation expectation rate')
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    display_data()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
