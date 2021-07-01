import os
import sys
import datetime

from flask import flash, redirect, render_template, request, session, \
    send_from_directory, abort
from flask_session import Session
from tempfile import mkdtemp
from chezmahe import app
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from chezmahe.models.sql_models import coin_history, get_topten, get_calls, \
    get_rows, count_names, first_call, insert_new, new_user, query_username, \
    get_ai, buy_item, sell_item, query_user_data, query_history, got_prediction, \
    get_user_id, coin_price_history, query_predictions
from chezmahe.config import Config
from chezmahe.models.helpers_cmc import apology, breakup_datetime, change_datetime
from chezmahe.models.users.user_models import login_required, lookup, use_prediction
from chezmahe.models.users.user_api import get_today



# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
#app.config["SESSION_FILE_DIR"] = mkdtemp()
#app.config["SESSION_PERMANENT"] = False
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config["DB_PATH"] = "/home/marc/cmcapps/cmcapps"
Session(app)


@app.route("/")
def index():
    """If logged in show porfolio else show index """

    if session.get("user_id") is None:
        # Get current AI values
        highs = get_ai()

        # Make a list of highscores
        high = list(range(len(highs)))
        for i in range(len(highs)):
            high[i] = {
                "username": highs[i][0],
                "total": highs[i][1]
            }
        length = len(highs)

        return render_template("index.html", highs=high, length=length)

    else:
        # Get current AI values
        highs = get_ai()

        # Make a list of highscores
        high = list(range(len(highs)))
        for i in range(len(highs)):
            high[i] = {
                "username": highs[i][0],
                "total": highs[i][1]
            }
        length_ai = len(highs)

        #print(f"highs = {highs}")
        #print(f"length = {length_ai}")

        # Get user's current holdings
        user_id = session["user_id"]
        result = query_user_data(user_id)
        items = result["items"]
        length = result["length"]
        cash = result["cash"]
        totalCash = result["totalCash"]

        return render_template("users/portfolio.html", highs=high, length_ai=length_ai, items=items, length=length, cash=cash, totalCash=totalCash)


@app.route("/charts", methods=["GET", "POST"])
def charts():
    """the charts"""

    # If method is POST
    if request.method == "POST":

        # what coin and range was selected
        coin = request.form.get("newcoin")
        dRange = request.form.get("daterange")

        # Get the coin history and available coins
        dRange, dateRange, available, coin, thevalue, dates, length = coin_history(coin, dRange)

        return render_template("charts.html",dRange=dRange, dateRange=dateRange, available=available, coin=coin, thevalue=thevalue, dates=dates, length = length)

    # If method is Get
    else:
        # Use bitcoin and All Time as default.
        coin = "Bitcoin"
        dRange = "All Time"

        # Get the coin history and available coins
        dRange, dateRange, available, coin, thevalue, dates, length = coin_history(coin, dRange)


        return render_template("charts.html", dRange=dRange, dateRange=dateRange, available=available, coin=coin, thevalue=thevalue, dates=dates, length = length)


@app.route("/topten")
def topten():
    """show top ten"""

    # Get most recent 10 rows
    coins, date = get_topten("cmc")

    return render_template("topten.html", coins = coins , date = date)


@app.route("/stocks")
def stocks():
    """show top ten stocks"""
    theStocks = get_topten("iex")

    return render_template("stocks.html", theStocks = theStocks)


@app.route("/bio")
def statistics():
    """show statistics"""

    # Number of api calls made
    calls = get_calls("cmc")
    calls += get_calls("iex")

    # Number of rows
    rows = get_rows("cmc")
    rows += get_rows("iex")

    # Number of distinct coins/stocks
    stocks = count_names("iex")
    coins = count_names("cmc")

    # Date of first call
    start_date = first_call()

    return render_template("bio.html", calls = calls, rows = rows, coins = coins,
        stocks = stocks, start_date = start_date)


@app.route("/receive", methods=['POST']) #Get will be blocked
def receive():
    """Receive json data for database. Update stocks or market."""

    # Authenticate with keys
    auth = request.headers.get("Authorization")
    #auth = headers.get("cm_key")
    correct = Config.CM_KEY
    #expected = Config.TEST
    if auth != correct:
        return jsonify({"message": "Unauthorized"}), 401
    else:

        # Keys are good, continue
        req_data = request.get_json()

        check = insert_new(req_data)

    if check:
        return ''' Success '''

    else:
        return ''' Failure: Type not recognized '''

@app.route("/download")
def download():
    """Download current .db"""

    try:
        return send_from_directory(app.config["DB_PATH"], "crypto.db",
            as_attachment = True)
    except FileNotFoundError:
        abort(404)


@app.route("/current")
def current():
    """ Send JSON of most recent prices etc. """


    # Authenticate with keys
    user = request.headers.get("username")
    pswd = request.headers.get("password")

    # Query database for username
    rows = query_username(user)

    # Ensure username exists and password is correct
    if len(rows) != 1 or not check_password_hash(rows[0][2], pswd):
        return apology("invalid username and/or password", 403)

    else:
        # Get most recent data
        data = get_today()

        return data


@app.route("/prediction", methods=["POST"])
def prediction():
    """ Receive AI prediction and update tables. """

    # Authenticate with keys
    user = request.headers.get("Username")
    pswd = request.headers.get("Password")

    # Query database for username
    rows = query_username(user)

    # Ensure username exists and password is correct
    if len(rows) != 1 or not check_password_hash(rows[0][2], pswd):
        return apology("invalid username and/or password", 403)


    # Username/password work.
    user_id = rows[0][0]
    req_data = request.get_json()
    check = got_prediction(user_id, req_data)

    if check:
        """ what to do with prediction goes here """

        choice = use_prediction(req_data["prediction"])
        if choice == "Do nothing":
            print("Doing nothing")
            return ''' Do nothing '''

        elif choice == "Buy":
            """ Use multiplier * cash to buy BTC """
            print("Buying")
            multiplier = 0.3
            result = query_user_data(user_id)
            cash = result["cash"] * multiplier
            type = "cmc"
            symbol = "BTC"

            # Get stock or coin info info
            item = lookup(type, symbol)
            shares = round(cash/item["price"], 2)

            # Update database with purchase info
            buy = buy_item(user_id, type, item, shares)

            if buy == True:
                return ''' Bought BTC '''
            else:
                return ''' Error on buy '''

        elif choice == "Sell":
            """ Use multiplier * BTC to sell BTC """
            print("Selling")
            multiplier = 0.3
            result = query_user_data(user_id)
            items = result["items"]
            #Make sure user HAS some btc
            if not items or items[0].shares <= 0:
                return ''' No BTC to sell '''
            else:
                to_sell = items[0].shares * multiplier
            type = "cmc"
            symbol = "BTC"

            # Get stock or coin info info
            item = lookup(type, symbol)

            # Update database with purchase info
            sell = sell_item(user_id, type, item, to_sell)

            if sell == True:
                return ''' Sold BTC '''
            else:
                return ''' Error on sell '''

        else:
            return ''' Error on choice '''

    else:
        return ''' Failure on check '''


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reched route via POST
    if request.method == "POST":

        # Ensure username submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure confirmation submitted
        elif not request.form.get("confirmation"):
            return apology("must re-enter password", 403)

        # Ensure password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match", 403)

        # Ensure password submitted
        elif not request.form.get("secretCode"):
            return apology("must provide Secret Code", 403)

        # Authenticate with keys
        auth = request.form.get("secretCode")
        correct = Config.SECRET_CODE
        if auth != correct:
            return apology("Incorrect secret code", 403)

        # Create new table entry for user
        username = request.form.get("username")
        password = request.form.get("password")
        hashword = generate_password_hash(password)
        new_user(username, hashword)

        return redirect("/")

    # User reached page via GET
    else:
        return render_template("users/register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login user"""

    # Forget any user_id
    session.clear()

    # User reached page via POST
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        user = request.form.get("username")

        # Query database for username
        rows = query_username(user)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Redirect user to home page
        return redirect("/")

    # User reached page via GET
    else:
        return render_template("users/login.html")


@app.route("/logout")
def logout():
    """Log user our"""
    session.clear()

    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get crypto or stock quote"""

    # If page reached via POST
    if request.method == "POST":
        type = request.form.get("type")
        symbol = request.form.get("symbol")

        # Ensure a ticker was entered
        if not symbol:
            return apology("must enter ticker symbol", 403)

        value = lookup(type, symbol)
        companyName = value["name"]
        price = value["price"]
        theSymbol = value["symbol"]
        theChange = value["p24"]

        return render_template("users/quoted.html", symbol=symbol, companyName=companyName,
            price=price, theSymbol=theSymbol, theChange=theChange)

    # If page reached via GET
    else:
        return render_template("users/quote.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy a coin or stock"""

    # User reached via POST
    if request.method == "POST":

        type = request.form.get("type")
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        user_id = session["user_id"]

        # Ensure symbol submitted
        if not symbol:
            return apology("must provide a symbol", 403)

        # Ensure positive number of shares
        elif shares <= "0":
            return apology("must provide positive number of shares", 403)

        # Get stock or coin info info
        item = lookup(type, symbol)

        # Ensure the ticker is real
        if not lookup(type, symbol):
            return apology("that's not a real ticker", 403)

        # Update database with purchase info
        buy = buy_item(user_id, type, item, shares)
        if buy == True:
            return redirect("/")
        else:
            return apology("you do not have enough money", 403)

    # User reached via GET
    else:
        return render_template("users/buy.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell a coin or stock"""

    # User reached via POST
    if request.method == "POST":

        type = request.form.get("type")
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        user_id = session["user_id"]

        # Ensure symbol submitted
        if not symbol:
            return apology("must provide a symbol", 403)

        # Ensure positive number of shares
        elif shares <= "0":
            return apology("must provide positive number of shares", 403)

        # Get stock info
        item = lookup(type, symbol)

        # Ensure the ticker is real
        if not lookup(type, symbol):
            return apology("that's not a real ticker", 403)

        sell = sell_item(user_id, type, item, shares)
        if sell == True:
            return redirect("/")
        else:
            return apology("You don't own that amount of that item", 403)

    # User reached via GET
    else:
        return render_template("users/sell.html")


@app.route("/history", methods=["GET"])
@login_required
def history():
    """Get trade history for user"""
    user_id = session["user_id"]
    result = query_history(user_id)

    return render_template("users/history.html", trans=result["trans"], length=result["length"])


@app.route("/mark1")
def mark1():
    """Get prediction history for mark1. Get actual BTC price history. Make a list
    with date, predicted, and find a matching actual price for predicted date if exists."""

    user_id = get_user_id("Mark1")
    start_date, predictions = query_predictions(user_id)
    length = len(predictions)
    btc_date, btc_price = coin_price_history("BTC", start_date)
    compare = []
    for i in range(len(predictions)):
        start_year, start_month, start_day = breakup_datetime(predictions[i]["date"])
        new_date = str(change_datetime(start_year, start_month, start_day, 3))
        if new_date in btc_date:
            index = btc_date.index(new_date)
            actual = round((btc_price[index] - btc_price[index - 3]) / btc_price[index -3], 3)
            compare.append({
                "date": new_date,
                "prediction": predictions[i]["prediction"],
                "actual": actual
            })
        else:
            compare.append({
                "date": new_date,
                "prediction": predictions[i]["prediction"],
                "actual": "N/A"
            })

    return render_template("users/mark1.html", length=length, predictions=compare)



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
