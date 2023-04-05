#!/usr/bin/env python3

from flask import Flask, json


from Symbols import Symbols 

symbolList = []

api = Flask(__name__)

# Normally you'd request a token and pass that back but the list of all stock symbols is not guarded information.

@api.route('/rest/v1/SymbolNames', methods=['GET'])
def get_companies():
  return json.dumps(symbolList)

if __name__ == '__main__':
  d = Symbols(".")
  symbolList = d.SymbolsList()
  api.run(host='0.0.0.0',port=7000)
