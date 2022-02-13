import sqlite3
import datetime
import pytz
import json
from cmcapps.models.helpers_cmc import Coin_short, Item, Transaction, Stock_short
from cmcapps.models.users.user_models import lookup


# Add database
db = sqlite3.connect('cmcapps/crypto.db', check_same_thread=False)

# Make sure it loaded
if not db:
    print("Could not load database")
    sys.exit(1)

cur = db.cursor()

def coin_history(coin, dRange):
    """Lookup for a single coin in the db. Provides a version for one month,
    week, day and the entire db range for that coin. Used by /chart"""

    # What are the available coin options
    current = cur.execute("SELECT DISTINCT name FROM market")
    result = current.fetchall()

    # Make list of available Coins
    length = len(result)
    available = list(range(length))
    for i in range(length):
        available[i] = result[i][0]

    # Make a list of available date ranges
    dateRange = ["All Time", "One Month", "One Week", "24 Hours"]

    # Get the data for selected Coin and Range
    if dRange == "All Time":
        current = cur.execute("SELECT * FROM market WHERE name=? ORDER BY id DESC",(coin,))
        result = current.fetchall()
    elif dRange == "One Month":
        current = cur.execute("SELECT * FROM market WHERE name=? ORDER BY id DESC LIMIT 730",(coin,))
        result = current.fetchall()
    elif dRange == "One Week":
        current = cur.execute("SELECT * FROM market WHERE name=? ORDER BY id DESC LIMIT 168",(coin,))
        result = current.fetchall()
    else:
        current = cur.execute("SELECT * FROM market WHERE name=? ORDER BY id DESC LIMIT 24",(coin,))
        result = current.fetchall()

    # Reverse result so that chart is cronological
    result.reverse()

    # Format data for chart
    length = len(result)
    thevalue = list(range(length))
    stuff = list(range(length))
    dates = list(range(length))
    counter = list(range(length))
    for i in range(length):
        thevalue[i] = round(result[i][7], 2)
        dates[i] = (result[i][1][0:10])
        counter[i] = float(i)

    return dRange, dateRange, available, coin, thevalue, dates, length


def coin_price_history(symbol, start_date):
    """ Pull datetime and price for given coin. One entry for each day. """

    # Get rows
    # current = cur.execute("SELECT datetime, price FROM market WHERE symbol = ? AND datetime >= ? AND datetime LIKE ('%23:0%')", (symbol, start_date,))
    # needed this row to test, use the other one?
    current = cur.execute("SELECT datetime, price FROM market WHERE symbol = ? AND datetime LIKE ('%15:0%') AND datetime >= ?", (symbol, start_date,))
    result = current.fetchall()
    print("result ", result)

    # Format needed data
    date = []
    price = []
    for i in range(len(result)):
        date.append(result[i][0][0:10])
        price.append(result[i][1])

    return date, price



def query_most_recent(type, name):
    """Get most recent data for... Used by /download"""

    if type == "cmc":
        current = cur.execute("SELECT datetime, symbol, price, volume_24h FROM market WHERE name=? ORDER BY id DESC LIMIT 61",(name,))
        result = current.fetchall()
    else:
        current = cur.execute("SELECT datetime, symbol, price, volume_24h FROM stocks WHERE name=? ORDER BY id DESC LIMIT 61",(name,))
        result = current.fetchall()

    return result


def get_ai():
    """Get current ai scores. """

    cur.execute('''CREATE TABLE IF NOT EXISTS users(
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    hash TEXT NOT NULL,
                    cash NUMERIC NOT NULL DEFAULT 100000.00,
                    total NUMERIC NOT NULL DEFAULT 100000.00
                    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS trades(
                    id INTEGER NOT NULL PRIMARY KEY,
                    user_id NUMERIC NOT NULL,
                    buysell TEXT NOT NULL,
                    type TEXT NOT NULL,
                    ticker TEXT NOT NULL,
                    units INTEGER NOT NULL,
                    price INTEGER NOT NULL,
                    datetime DATETIME NOT NULL
                    )''')

    cur.execute('''CREATE UNIQUE INDEX IF NOT EXISTS username ON users(
                    username
                    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS ai(
                    id INTEGER NOT NULL PRIMARY KEY,
                    user_id NUMERIC NOT NULL,
                    datetime DATETIME NOT NULL,
                    prediction NUMERIC NOT NULL
                    )''')

    current = cur.execute("SELECT username, total FROM users WHERE username = 'Mark1'")
    highs = current.fetchall()

    return highs


def query_predictions(user_id):
    """ Get list of past predictions/dates. """

    # Date of first prediction
    current = cur.execute("SELECT datetime FROM ai WHERE user_id=? LIMIT 1",(user_id,))
    result = current.fetchall()
    first_date = result[0][0][0:10]

    # The predictions
    current = cur.execute("SELECT datetime, prediction FROM ai WHERE user_id=?",(user_id,))
    result = current.fetchall()
    predictions = list(range(len(result)))
    for i in range(len(result)):
        predictions[i] = {
            "date": result[i][0][0:10],
            "prediction": result[i][1]
        }

    # The actual prices

    return first_date, predictions


def get_user_id(username):
    """ Return user id number. """

    current = cur.execute("SELECT id FROM users WHERE username=?",(username,))
    result = current.fetchall()
    id = result[0][0]

    return id


def get_topten(type):
    """ Get top ten of coins or stocks. """

    if type == "cmc":
        # Get most recent 10 rows from coins
        current = cur.execute("SELECT * FROM market ORDER BY id DESC LIMIT 10")
        result = current.fetchall()

        # Make a list of coins and round dollar value
        coins = list(range(len(result)))
        for i in range(len(result)):
            coins[i] = Coin_short(
                result[i][3],
                result[i][4],
                round(result[i][7],2),
                result[i][8]
                )
        date = result[0][1]

        return coins, date

    else:
        # Get most recent 10 rows
        #current = cur.execute("SELECT * FROM stocks ASC GROUP BY name, date ORDER BY name DESC")
        current = cur.execute("SELECT * FROM stocks GROUP BY name ORDER BY name DESC")
        result = current.fetchall()

        # Make a list of coins and round dollar value
        # theStocks = list(range(len(result)))
        name = result[0][0]

        theStocks = list(range(len(result)))
        for i in range(len(result)):
            theStocks[i] = Stock_short(
                result[i][1],
                result[i][2],
                result[i][3],
                result[i][4]
                )

        return theStocks


def get_calls(type):
    """ Return the number of api calls for the given type. """

    # stocks
    if type == "iex":
        current = cur.execute("SELECT COUNT(DISTINCT date) FROM stocks")
        result = current.fetchall()
        calls = result[0][0]
    # cryptocurrency
    else:
        current = cur.execute("SELECT COUNT(DISTINCT datetime) FROM market")
        result = current.fetchall()
        calls = result[0][0]

    return calls


def get_rows(type):
    """ Return the number of rows for the given type. """

    # stocks
    if type == "iex":
        # Number of rows
        current = cur.execute("SELECT COUNT(name) FROM stocks")
        result = current.fetchall()
        rows = result[0][0]

    # Coins
    else:
        current = cur.execute("SELECT COUNT(name) FROM market")
        result = current.fetchall()
        rows = result[0][0]

    return rows


def count_names(type):
    """ Return the number of distinct names for each type. """

    # Stocks
    if type == "iex":
        # Number of distinct coins/stocks
        current = cur.execute("SELECT COUNT(DISTINCT name) FROM stocks")
        result = current.fetchall()
        count = result[0][0]

    # Coins
    else:
        current = cur.execute("SELECT COUNT(DISTINCT name) FROM market")
        result = current.fetchall()
        count = result[0][0]

    return count


def first_call():
    """ Date of first call."""

    current = cur.execute("SELECT datetime FROM market ASC LIMIT 1")
    result = current.fetchall()
    start_date = result[0][0]

    return start_date


def insert_new(req_data):
    """ Add new row to market or stocks, create table if needed. """

    # Break up data into parts
    keys = req_data.keys()
    for key in keys:
        # Stocks
        if req_data[key]["type"] == "iex":
            type = req_data[key]["type"]
            name = req_data[key]["name"]
            symbol = req_data[key]["symbol"]
            price = req_data[key]["price"]
            # date = req_data[key]["date"]

            utc_now = pytz.utc.localize(datetime.datetime.utcnow())
            adt_now = utc_now.astimezone(pytz.timezone('America/Halifax'))

            date = adt_now

            # If stocks table doesn't exist, create it.
            cur.execute('''CREATE TABLE IF NOT EXISTS stocks(
                            id INTEGER NOT NULL PRIMARY KEY,
                            name TEXT,
                            symbol TEXT,
                            price INTEGER,
                            date TEXT
                            )''')

            # Put it into correct database
            cur.execute("INSERT INTO stocks (name, symbol, price, date) VALUES (?,?,?,?)", (name, symbol, price, date))

        # Coins
        elif req_data[key]["type"] == "cmc":
            # Make a list of coins
            coins = list(range(len(req_data['data'])))
            # print(len(data['data']))
            for i in range(len(data['data'])):
                coins[i] = Coin(
                    data['data'][i]['id'],
                    data['data'][i]['name'],
                    data['data'][i]['symbol'],
                    data['data'][i]['max_supply'],
                    data['data'][i]['circulating_supply'],
                    data['data'][i]['quote']['USD']['price'],
                    data['data'][i]['quote']['USD']['volume_24h']
                    )

            # set time
            utc_now = pytz.utc.localize(datetime.datetime.utcnow())
            adt_now = utc_now.astimezone(pytz.timezone('America/Halifax'))

            # Iterate through coins to make a new row for each coin
            for i in range(len(coins)):

                cur.execute("INSERT INTO market (datetime, coin_id, name, symbol, max_supply, circulating_supply, price, volume_24h) VALUES (?,?,?,?,?,?,?,?)", (
                        adt_now, coins[i].id, coins[i].name, coins[i].symbol, coins[i].max_supply, coins[i].circulating_supply, coins[i].price, coins[i].volume_24h))

            # Add index for symbol
            cur.execute("CREATE INDEX IF NOT EXISTS idx_symbol ON market (symbol)")

        else:
            return False

    db.commit()
    return True


def new_user(username, hashword):
    """Add new user to database. Used to refister a new user."""

    cur.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hashword))

    db.commit()

    return


def query_username(user):
    """Query database for username. Used during login."""

    current = cur.execute("SELECT * FROM users WHERE username = ?", (user,))
    rows = current.fetchall()

    return rows


def query_user_data(user_id):
    """Query current user holdings. """

    items = []
    totalCash = 0

    # Load users portfolio
    current = cur.execute("SELECT DISTINCT ticker, type FROM trades WHERE user_id= ?", (user_id,))
    tickers = current.fetchall()

    # Append items with new Item
    for i in range(len(tickers)):
        type = tickers[i][1]
        ticker = tickers[i][0]
        value = lookup(type, ticker)
        companyName = value["name"]
        price = value["price"]
        current = cur.execute("SELECT COALESCE((SELECT SUM(units) FROM trades WHERE buysell == 'buy' AND type = ? AND ticker = ? AND user_id= ?), 0) - COALESCE((SELECT SUM(units) FROM trades WHERE buysell == 'sell' AND type = ? AND ticker = ? AND user_id = ?), 0) AS 'shares'",
                           (type, ticker, user_id, type, ticker, user_id,))
        share = current.fetchall()
        total = round(share[0][0] * price, 2)
        items.append(Item(type, ticker, companyName, share[0][0], price, total))
        totalCash += round(total, 2)

    length = len(items)
    current = cur.execute("SELECT cash FROM users WHERE id= ?", (user_id,))
    row = current.fetchall()
    cash = round(row[0][0])
    totalCash += cash
    cur.execute("UPDATE users SET total = ? WHERE id= ?", (totalCash, user_id,))
    db.commit()

    return {
        "items": items,
        "length": length,
        "cash": cash,
        "totalCash": totalCash
    }


def query_history(user_id):
    """ Show history of transactions for user. """
    trans = []

    # Get all transactions for current user
    current = cur.execute("SELECT buysell, type, ticker, units, price, datetime FROM trades WHERE user_id = ?",
                      (user_id,))
    rows = current.fetchall()

    # Iterate through to make a Transaction for each class and append to trans
    for i in range(len(rows)):
        trans.append(Transaction(rows[i][0], rows[i][1], rows[i][2], rows[i][3], rows[i][4], rows[i][5]))

    # Get length of trans
    length = len(trans)

    return {
        "trans": trans,
        "length": length
    }


def buy_item(user_id, type, item, shares):
    """ Buy the thing """

    # Get current user values
    current = cur.execute("SELECT * FROM users WHERE id = ?",
                      (user_id,))
    rows = current.fetchall()

    # values
    username = rows[0][1]
    cash = rows[0][3]
    thesymbol = item["symbol"]
    sha = float(shares)
    new_cash = cash - (item["price"] * sha)

    # Ensure they have enough cash
    if new_cash < 0:
        return False

    # Update tables
    cur.execute("UPDATE users SET cash = ? WHERE id = ?", (new_cash, user_id,))
    cur.execute("INSERT INTO trades (user_id, buysell, type, ticker, units, price, datetime) VALUES(?,?,?,?,?,?,datetime('now'))",
               (user_id, "buy", type, item["symbol"], sha, item["price"],))

    db.commit()
    return True


def sell_item(user_id, type, item, shares):
    """ Sell the thing """

    # Get current user values
    current = cur.execute("SELECT * FROM users WHERE id = ?",
                      (user_id,))
    rows = current.fetchall()

    # values
    username = rows[0][1]
    cash = rows[0][3]
    thesymbol = item["symbol"]
    sha = float(shares)
    new_cash = cash + (item["price"] * sha)
    current = cur.execute("SELECT COALESCE((SELECT SUM(units) FROM trades WHERE buysell == 'buy' AND ticker = ? AND type = ? AND user_id = ?), 0) - COALESCE((SELECT SUM(units) FROM trades WHERE buysell == 'sell' AND ticker = ? AND type = ? AND user_id = ?), 0) AS 'shares'",
                         (thesymbol, type, user_id, thesymbol, type, user_id))
    rows = current.fetchall()

    # Ensure they actualy own that stock
    if not rows[0][0] or rows[0][0] == 0:
        return False

    # Ensure they have enough shares
    elif sha > rows[0][0]:
        return False

    # Update tables
    cur.execute("UPDATE users SET cash = ? WHERE id = ?", (new_cash, user_id,))
    cur.execute("INSERT INTO trades (user_id, buysell, type, ticker, units, price, datetime) VALUES(?,?,?,?,?,?,datetime('now'))",
               (user_id, "sell", type, item["symbol"], sha, item["price"],))
    db.commit()
    return True


def got_prediction(user_id, req_data):
    """Take the received AI prediction and process it. Insert into ai table the
    datetime, ai, and predicted value. """

    # If ai table doesn't exist, create it.
    cur.execute('''CREATE TABLE IF NOT EXISTS ai(
                    id INTEGER NOT NULL PRIMARY KEY,
                    user_id NUMERIC NOT NULL,
                    datetime DATETIME NOT NULL,
                    prediction NUMERIC NOT NULL
                    )''')

    prediction = req_data["prediction"]

    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    adt_now = utc_now.astimezone(pytz.timezone('America/Halifax'))

    cur.execute("INSERT INTO ai (user_id, datetime, prediction) VALUES(?,?,?)",
               (user_id, adt_now, req_data["prediction"],))

    db.commit()
    return True
