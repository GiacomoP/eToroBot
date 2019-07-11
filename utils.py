import math


__all__ = ["humanise_number", "format_ranked_stocks_by_volume", "format_ranked_stocks_with_price"]


_millnames = ["", " Thousand", " Million", " Billion"]


def humanise_number(n):
    """Based on https://stackoverflow.com/a/3155023"""
    millidx = max(0, min(len(_millnames) - 1, int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))))
    return "{:.2f}{}".format(n / 10 ** (3 * millidx), _millnames[millidx])


def format_ranked_stocks_by_volume(stocks):
    """
    Given a list of Stocks, the output will be:
    1. $LLOY.L 10.80 Million // 2. $TCG.L 9.27 Million // 3. $INDV.L 7.96 Million // ...
    """
    output = ""
    for index, stock in enumerate(stocks):
        output += f"{index + 1}. ${stock.etoro_symbol} {humanise_number(stock.volume)}"
        output += " // " if index != len(stocks) - 1 else ""
    return output


def format_ranked_stocks_with_price(stocks):
    """
    Given a list of Stocks, the output will be:
    1. $INDV.L 58.76 (+32.64%) // 2. $TCG.L 13.42 (+11.65%) // 3. $DPLM.L 1,393.00 (+3.80%) // ...
    """
    output = ""
    for index, stock in enumerate(stocks):
        output += f"{index + 1}. ${stock.etoro_symbol} {stock.last_price * 100:,.2f} ({stock.percent_change_previous_price:+.2f}%)"
        output += " // " if index != len(stocks) - 1 else ""
    return output
