#!/usr/bin/env python3

from flask import Flask, json


from StockTickerSymbols import StockTickerSymbols 

symbolListValid = False
symbolList      = []

api = Flask(__name__)

# Normally you'd request a token and pass that back but the list of all stock symbols is not guarded information.

@api.route('/rest/v1/StockTickerSymbols', methods=['GET'])
def get_companies():
  # Only returns 200 or 500.
  try: 
    if symbolListValid:
      return json.dumps({"Valid": True, "data": symbolList})
    else: 
      return json.dumps({"Valid": False,"Messages": [symbolList]})
  except Exception as e: 
    return json.dumps({"Messages": [str(e)]}),500  

if __name__ == '__main__':
  d = StockTickerSymbols(".")
  symbolListValid,symbolList = d.SymbolsList()
  api.run(host='0.0.0.0',port=7000)
