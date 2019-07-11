import copy
import logging
import requests

from models import StockParsingException


__all__ = ["fetch_all_stocks"]


logger = logging.getLogger(__name__)


def fetch_all_stocks(token, stocks, page_size=None):
    # Don't handle the referenced list directly
    stocks = copy.deepcopy(stocks)

    request_headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive"
    }

    request_params = {
        "_Token": token,
        "IdentifierType": "Symbol",
        "Identifiers": ""  # To fill in later due to pagination
    }

    session = requests.Session()

    # Paginated requests
    stocks_to_return = []
    call = 0
    while True:
        start = page_size * call

        if start > len(stocks):
            break

        number_of_items = page_size if start + page_size < len(stocks) else None
        request_params["Identifiers"] = ", ".join(stock.xignite_symbol for stock in stocks[start:number_of_items])
        call += 1

        prepared_request = requests.Request(method="GET", url="https://globalquotes.xignite.com/v3/xGlobalQuotes.json/GetGlobalExtendedQuotes", headers=request_headers, params=request_params).prepare()
        response = session.send(prepared_request).json()

        if not isinstance(response, list) or not response:
            raise ValueError("Xignite didn't return a list of stocks.")

        for xi_stock in response:
            for stock in stocks:
                if stock.xignite_symbol == xi_stock["Security"]["Symbol"]:
                    try:
                        stock.parse_from_xignite(xi_stock)
                        stocks_to_return.append(stock)
                    except StockParsingException:
                        logger.warning("{} couldn't be looked up on Xignite.".format(stock.name if stock.name else stock.xignite_symbol))
                        pass
                    break

    return stocks_to_return
