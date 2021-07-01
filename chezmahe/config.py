import os
import json

with open('/etc/chezmahe_config.json') as config_file:
	config = json.load(config_file)

class Config:
	CMC_KEY = config.get('X-CMC_PRO_API_KEY')
	IEX_KEY = config.get('iex_key')
	CM_KEY = config.get('cm_key')
	SECRET_CODE = config.get('secret_code')
