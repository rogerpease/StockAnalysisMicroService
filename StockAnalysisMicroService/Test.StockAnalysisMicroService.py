#!/usr/bin/env python3

import requests
import re

result = requests.get("http://10.0.0.150:7003/ByDividend.html") 
assert re.search("THIS IS NOT",result.text)
assert len(result.text.split("\n"))>100,result.text
assert print(result.text.split("\n")),result.text
