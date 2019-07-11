import datetime as dt
import pytz


class StockParsingException(Exception):
    """Raised when the data to improve knowledge of a Stock is invalid"""
    pass


class Stock(object):
    xignite_symbol = ""
    etoro_symbol = ""

    name = ""
    quote_date_time = None
    currency = ""
    volume = 0
    last_price = 0
    change_previous_price = 0
    percent_change_previous_price = 0

    def __init__(self, xignite_symbol, etoro_symbol):
        self.xignite_symbol = xignite_symbol
        self.etoro_symbol = etoro_symbol

    def parse_from_xignite(self, data):
        """Fills in more information about this stock from Xignite's data"""
        if data.get("Outcome") != "Success":
            if data.get("Security", {}).get("Name"):
                self.name = data["Security"]["Name"]
            raise StockParsingException

        self.name = data["Security"]["Name"]
        self.currency = data["Currency"]
        self.volume = data["Volume"]
        self.last_price = data["Last"]
        self.change_previous_price = data["ChangeFromPreviousClose"]
        self.percent_change_previous_price = data["PercentChangeFromPreviousClose"]

        # Transform the quote's date and time to UTC datetime
        utc_unaware_datetime = dt.datetime.strptime("{} {}".format(data["Date"], data["Time"]), "%m/%d/%Y %I:%M:%S %p") - dt.timedelta(hours=data["UTCOffset"])
        self.quote_date_time = pytz.utc.localize(utc_unaware_datetime)
