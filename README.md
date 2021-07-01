# CMCApps
My project, cmcapps, is a web based application. The main part of the application (run.py) provides the user  
interface. The index alows the user to view a chart of value in USD over time for any coin in the database.  
The Top Ten page shows the top ten cryptocurrencies by market capitalization from the most recent api call.  
Finally, the statistic pages gives some information about the current database.

The second part of the application is a python program that does an API call to coinmarketcap.com and inserts
the top ten crypto to the database. On my own personal cloud server I'm using crontab to run cmc_api.py every
hour.  

**Keys**  
The database updater cmc_api.py uses a coin market cap api key. It will look for your key in /etc/cmcapps_config.json  
Get your own key at https://coinmarketcap.com/api/  

To generate a random key in unix
tr -dc A-Za-z0-9 </dev/urandom | head -c 13 ; echo ''
