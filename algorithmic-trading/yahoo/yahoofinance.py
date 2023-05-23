import yfinance as yf


class YahooFinance:
    def __init__(self, ticker, start, end):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.stock = yf.Ticker(ticker)

    def get_history(self):
        return self.stock.history(start=self.start, end=self.end)

    def get_tail(self):
        return self.get_history().tail()

    def get_head(self):
        return self.get_history().head()
