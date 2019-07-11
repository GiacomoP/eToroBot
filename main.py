import datetime as dt
import locale
import logging
import operator

from settings import XIGNITE_TOKEN, XIGNITE_STOCK_LIMIT, STOCKS, LOGGING_LEVEL
from libs import xignite
from utils import format_ranked_stocks_by_volume, format_ranked_stocks_with_price


# Initial setup
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
logging.basicConfig(level=LOGGING_LEVEL)
logger = logging.getLogger(__name__)


stocks = xignite.fetch_all_stocks(XIGNITE_TOKEN, STOCKS, XIGNITE_STOCK_LIMIT)

volume_key = operator.attrgetter("volume")
percent_key = operator.attrgetter("percent_change_previous_price")

top_stocks_by_volume = sorted(stocks, key=volume_key, reverse=True)[:5]
best_stocks = sorted(stocks, key=percent_key, reverse=True)[:5]
worst_stocks = sorted(stocks, key=percent_key, reverse=False)[:5]

todays_date = dt.datetime.utcnow().strftime("%A %d %B")
message = ">> \U0001F1EC\U0001F1E7  DAILY performance of LONDON's stocks \U0001F1EC\U0001F1E7  <<\n" \
    f"After analysing {len(stocks)} stocks in the London Stock Exchange, the following " \
    f"are the TOP 5 traded stocks by volume for TODAY {todays_date}:\n" \
    f"{format_ranked_stocks_by_volume(top_stocks_by_volume)}.\n\n" \
    "In addition, the following are the 5 BEST GAINERS:\n" \
    f"{format_ranked_stocks_with_price(best_stocks)}.\n\n" \
    "Finally, here are the 5 WORST LOSERS:\n" \
    f"{format_ranked_stocks_with_price(worst_stocks)}." \

logger.info(message)
