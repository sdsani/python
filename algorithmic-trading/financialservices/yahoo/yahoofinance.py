import yfinance as yf
from financialservices.financeservice import FinanceService


class YahooFinance(FinanceService):
    def __init__(self, ticker, start, end, sma1, sma2):
        self.start = start
        self.end = end
        FinanceService.__init__(self, ticker, 'Adj Close', sma1, sma2)

    def load_financial_data(self):
        self.stock_data = yf.download(self.ticker, start=self.start, end=self.end)
        self.build_simple_moving_average()
        self.build_dual_signal_data()





