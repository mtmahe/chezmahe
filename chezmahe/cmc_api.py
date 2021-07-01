from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import sqlite3
from models.helpers_cmc import Coin
import datetime
import pytz
from config import Config

# degault from Coin Market Cap website
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'10',
  'convert':'USD'
}
# replaced key with link
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': Config.CMC_KEY,
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  # print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

# Make a list of coins
coins = list(range(len(data['data'])))
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
    # print(coins[i].name)

# Open or create db
db = sqlite3.connect('/home/marc/cmcapps/cmcapps/crypto.db')

# Make sure it loaded
if not db:
    print("Could not load database")
    sys.exit(1)

cur = db.cursor()

# cur.execute("DROP TABLE IF EXISTS market")

# set time
utc_now = pytz.utc.localize(datetime.datetime.utcnow())
adt_now = utc_now.astimezone(pytz.timezone('America/Halifax'))
print(adt_now)

# Iterate through coins to make a new row for each coin
for i in range(len(coins)):
    print(f'\nAdding {coins[i].name} to table')
    print(datetime.datetime.now())
    cur.execute('''CREATE TABLE IF NOT EXISTS market(
                    id INTEGER NOT NULL PRIMARY KEY,
                    datetime TEXT,
                    coin_id INTEGER,
                    name STRING,
                    symbol STRING,
                    max_supply,
                    circulating_supply INTEGER,
                    price INTEGER,
                    volume_24h INTEGER
                    )''')

    cur.execute("INSERT INTO market (datetime, coin_id, name, symbol, max_supply, circulating_supply, price, volume_24h) VALUES (?,?,?,?,?,?,?,?)", (
                adt_now, coins[i].id, coins[i].name, coins[i].symbol, coins[i].max_supply, coins[i].circulating_supply, coins[i].price, coins[i].volume_24h))

# Add index for symbol
cur.execute("CREATE INDEX IF NOT EXISTS idx_symbol ON market (symbol)")
db.commit()
