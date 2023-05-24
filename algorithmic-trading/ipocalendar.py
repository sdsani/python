from financialservices.alphavantage.IPOCalendar import IPOCalendar

av = IPOCalendar(use_free_service=True)
print(av.get_ipo_calendar())
