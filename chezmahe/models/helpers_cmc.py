import os
import datetime

from flask import render_template


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def breakup_datetime(datetime):
    """ Separate datetime into year, month, day. """

    year = datetime[0:4]
    month = datetime[5:7]
    day = datetime[8:10]

    return year, month, day


def change_datetime(start_year, start_month, start_day, change):
    """ Change date by 'change' number of days. """

    d = datetime.date(int(start_year), int(start_month), int(start_day))
    delta = datetime.timedelta(change)
    new_date = d + delta

    return new_date


class Coin:
    def __init__(self, id, name, symbol, max_supply, circulating_supply, price, volume_24h):
        self.id = id
        self.name = name
        self.symbol = symbol
        self.max_supply = max_supply
        self.circulating_supply = circulating_supply
        self.price = price
        self.volume_24h = volume_24h


class Coin_short:
    def __init__(self, name, symbol, price, volume_24h):
        self.name = name
        self.symbol = symbol
        self.price = price
        self.volume_24h = volume_24h


class Item:
    def __init__(self, type, ticker, name, shares, price, total):
        self.type = type
        self.ticker = ticker
        self.name = name
        self.shares = shares
        self.price = price
        self.total = total


class Stock_short:
    def __init__(self, name, symbol, price, date):
        self.name = name
        self.symbol = symbol
        self.price = price
        self.date = date


# Class to pass to history
class Transaction:
    def __init__(self, buysell, type, ticker, units, price, date):
        self.buysell = buysell
        self.type = type
        self.ticker = ticker
        self.units = units
        self.price = price
        self.date = date
