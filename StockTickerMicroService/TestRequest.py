#!/usr/bin/env python3

import requests
import os

assert("STOCKMICROSERVICEIPADDR" in os.environ) 
ip=os.environ["STOCKMICROSERVICEIPADDR"]

result = requests.get("http://10.0.0.150:7000/rest/v1/StockTickerSymbols") 
assert "Valid" in result.json()
assert result.json()["Valid"]
assert len(result.json()["data"]) > 100 
assert result.status_code == 200 


