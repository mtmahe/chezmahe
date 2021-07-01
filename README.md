# Chez Mahe
My project, chezmahe, is a web based application. The main part of the application (run.py) provides the user  
interface. Charts alows the user to view a chart of value in USD over time for any coin in the database.  
The Top Crypto page shows the top ten cryptocurrencies by market capitalization from the most recent api call. 
Top Stocks is the same but for stocks. Finally, the statistic pages gives some information about the current database.
If a user logs in they will also be able to look up prices, buy and sell.

My running version also has an AI trained with Keras TensorFlow to make it's own trades. You'll see the API info but 
the AI is not included in this repository.

The second part of the application is a python program that does an API call to coinmarketcap.com and inserts
the top ten crypto to the database. You could use crontab to run cm_api.py every hour. My personal site is updated 
through API, see Usage below.

**Keys**  
The database updater cm_api.py uses a coin market cap api key. It will look for your key in /etc/chezmahe_config.json  
Get your own key at https://coinmarketcap.com/api/  
Similarly you can get the stock API information here https://iextrading.com/api-terms/

**Usage**  
The preferred way to update the database is by API although you can just use cm_api mentioned above.

Endpoints:
'http://[your_site_name].com/receive', data = jsonData, headers=newHeaders

newHeaders = {'Content-type': 'application/json',
    'Authorization': cm_key,
    'Accept': 'text/plain'
    }
    
The server will be expecting json data with: type, name, symbol, price and date for each coin or stock.  
Type: iex (stock) or cmc (crypto)  
name: eg. Bitcoin  
Ticker: eg. BTC  
price: eg. 33000.33  
date: pytz format datetime

cm_key: should match your config file. You get to pick it.

To generate a random key in unix
tr -dc A-Za-z0-9 </dev/urandom | head -c 13 ; echo ''


For the AI:  
urlGet = 'http://[your_site_name].com/current'  
urlPost = 'http://[your_site_name].com/prediction'  

You'll need to use:  
headers = {  
		'Accepts': 'application/json',  
		'username': username,  
		'password': password  
	}  
as well as 'prediction' for the urlPost.  

If you wish to change how the site uses the prediction look at the prediction route. Eventually that 
will be moved into the 'models' folder. By default it's very pessimistig but my AI hasn't seen a market 
crash yet...  

Thanks for reading and I hope you enjoy!
