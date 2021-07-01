import json
import requests
import datetime

from cmcapps.models.sql_models import query_most_recent

def get_today():
    """ Gets last 61 days of data then uses it to append
    most recent row with moving avg etc and returns more complete
    version of only today's data. """

    def new_sma(data, c, n):
        """ Append a moving average of price, from column c, of lenght n"""
        for i in range(len(data)):
            if i < (n - 1):
                data[i].append(None)
            else:
                sma = 0
                for j in range(i - (n-1), i):
                    sma += data[j][c]
                sma = round((sma / n), 2)
                data[i].append(sma)

        return data

    data = query_most_recent("cmc", "Bitcoin")

    # Round the price to 2 decimal points
    for i in range(len(data)):
        data[i] = list(data[i])
        data[i][2] = round(data[i][2], 2)

    # Add 24hr % change
    for i in range(len(data)):
        # Add Null first so there are missing columns
        if i < 1:
            data[i].append(None)
        else:
            data[i].append((data[i][2] - data[i-1][2]) / data[i-1][2])

    data = new_sma(data, 2, 10)
    data = new_sma(data, 2, 60)

    eth = query_most_recent("cmc", "Ethereum")

    # Round price to 2 decimals and switch from tuple to list
    for i in range(len(eth)):
        eth[i] = list(eth[i])
        eth[i][2] = round(eth[i][2], 2)

    # Get the number of columns in current table (new price column will be that plus 3)
    x = len(data[0])

    # Add eth to chart
    for i in range(len(data)):
        for j in range(len(eth[0])):
            data[i].append(eth[i][j])

    data = new_sma(data, 9, 10)
    data = new_sma(data, 9, 60)

    # Get the weekday
    for i in range(len(data)):
        year = (int(data[i][0][0:4]))
        month = (int(data[i][0][5:7]))
        day = (int(data[i][0][8:10]))
        wkday = datetime.datetime(year, month, day).weekday()
        data[i].append(wkday)

    # It's built now just take the last row
    data = data[-1]
    data = json.dumps(data)

    return data
