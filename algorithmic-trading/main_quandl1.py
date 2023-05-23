import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import quandl

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

plt.style.use('seaborn')
start = datetime(2020, 1, 1)
end = datetime(2023, 5, 1)

investor_sentiment = quandl.get('AAII/AAII_SENTIMENT', start_date= start, end_date= end)
investor_sentiment['Bull-Bear Spread'].plot(figsize=(20,5), title='American Association of Individual Investor bull-bear spread sentiment'), plt.show();
investor_sentiment.tail()