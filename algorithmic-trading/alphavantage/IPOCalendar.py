import requests
import csv
import pandas as pd


class IPOCalendar:
    # Free service params
    free_key = 'SQZSDKNR18C8UYOW'

    premium_key = 'demo'

    base_url = 'https://www.alphavantage.co/query?function='
    stock_data_url = '{base_url}{function}&symbol={ticker}&apikey={key}'
    ipo_calendar = '{base_url}IPO_CALENDAR&apikey={key}'

    use_free_service = True

    def __init__(self, use_free_service):
        self.__class__.use_free_service = use_free_service


    def get_api_key(self):
        if self.__class__.use_free_service:
            return self.__class__.free_key
        else:
            return self.__class__.premium_key

    def get_ipo_calendar(self):
        url = self.__class__.ipo_calendar.format(base_url=self.__class__.base_url, \
                                                 key=self.get_api_key())

        # print(url)
        with requests.Session() as s:
            download = s.get(url)
            decoded_content = download.content.decode('utf-8')
            data = list(csv.reader(decoded_content.splitlines(), delimiter=','))
            column_names = data.pop(0)
            return pd.DataFrame(data, columns=column_names)
