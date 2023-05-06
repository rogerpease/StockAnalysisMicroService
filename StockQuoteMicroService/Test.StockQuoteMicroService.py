#!/usr/bin/env python3

import requests
import json 

result = requests.get("http://10.0.0.150:7002/rest/v1/StockInfoByTicker",data=json.dumps({"Ticker": "TGAA"}))
print(result.json()) 
assert result.json()["Valid"]
