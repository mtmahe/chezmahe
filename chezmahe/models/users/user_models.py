import os
import requests
import urllib.parse

from flask import redirect, request, session
from functools import wraps
from cmcapps.config import Config
from cmcapps.models.helpers_cmc import Coin
from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError

# API info
cmc_key = Config.CMC_KEY
iex_key = Config.IEX_KEY


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(type, symbol):
    """Look up quote for symbol based on iex or cmc type."""

    symbol = symbol.upper()

    # Check Type
    if type == "iex":
        # Contact iex API
        try:
            response = requests.get(f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={iex_key}")
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"error in request: {e}")
            return None

        # Parse response
        try:
            quote = response.json()
            #print(f"quote = {quote}")
            return {
                "name": quote["companyName"],
                "price": float(quote["latestPrice"]),
                "symbol": quote["symbol"],
                "p24": quote["changePercent"]
            }

        except (KeyError, TypeError, ValueError):
            print("error in lookup")
            return None

    # Type is cmc
    else:
        # Contact cmc API
        try:
            cmc = CoinMarketCapAPI(cmc_key)
            response = cmc.cryptocurrency_quotes_latest(symbol=symbol)
        except CoinMarketCapAPIError as e:
            print(f"error in request: {e}")
            return None

        # Parse response
        try:
            return {
                "name": response.data[symbol]["name"],
                "price": response.data[symbol]["quote"]["USD"]["price"],
                "symbol": symbol,
                "p24": response.data[symbol]["quote"]["USD"]["percent_change_24h"]
            }


        except (KeyError, TypeError, ValueError):
            print("error in lookup")
            return None


def use_prediction(prediction):
    """Check if prediction within perameters for Buy or Sell. """

    print("Reading prediction. Deciding what to do...")
    if prediction >= 0.5:
        return "Buy"

    elif prediction <= 0.2:
        return "Sell"

    else:
        return "Do nothing"
