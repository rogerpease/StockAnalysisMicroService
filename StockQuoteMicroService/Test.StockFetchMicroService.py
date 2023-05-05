#!/usr/bin/env python3

import requests
import json 

result = requests.get("http://10.0.0.150:7001/Log")
assert(len(result.text.split("\n"))>4),result.text.split("\n")
