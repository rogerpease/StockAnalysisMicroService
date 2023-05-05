#!/usr/bin/env python3 

from flask import Flask, json,request 
import time 
import requests
import os

import sys
sys.path.append("StockDataSets") 

from AlphaVantageDataSet import AlphaVantageDataSet

stockSymbolNames = [] 
d = AlphaVantageDataSet("/opt/nfs/StockDataCache") 

SHARESOUTSTANDING="SharesOutstanding" 
api = Flask(__name__)

#
# Get Critical Information (price, Dic Yield, etc)
#
#

def GetCriticalStockInformation(stockTickerSymbol):
  try: 
    data = {}
    overviewResult = d.MakeReq(sym=stockTickerSymbol,fn="OVERVIEW",doNotFetch=True) 
    if overviewResult != None and "data" in overviewResult: 
        overview = overviewResult["data"]
        myRes = {"Ticker": stockTickerSymbol}
        if "DividendYield" in overview:
          myRes["DividendYield"] =  overviewResult["data"]["DividendYield"] 
        if "MarketCapitalization" in overview and SHARESOUTSTANDING in overview and overview["MarketCapitalization"] is not None and overview["SharesOutstanding"] is not None\
           and overview["MarketCapitalization"] != "None"  and overview["SharesOutstanding"] != "None"  \
           and int(overview["SharesOutstanding"]) != 0:
          myRes["Price"] = float(int(overview["MarketCapitalization"])/int(overview["SharesOutstanding"])) 
        for field in ['52WeekHigh', '52WeekLow', '50DayMovingAverage']:
          if field in overview: 
            myRes[field] = overview[field]
        return {"Valid": True, "data": myRes}
    else:
      return {"Valid": False, "data": []}
           
  except Exception as e: 
    return json.dumps({"Valid": False,"Messages": [str(e)] })
  
  return {"Valid": True, "data": data}

#
# The super brillant algorithm that will make me rich. 
#
#
#
#
#

def IsAuthentic(jsonBody): 
  return True 

def IsAuthorized(jsonBody):
  return True 

@api.route('/rest/v1/StockInfoByTicker', methods=['GET'])
def get_companies():
  try:
    if not os.path.exists("/opt/nfs/StockDataCache"):
      return json.dumps({"Valid": False, "Messages": ["Stockdatacache not found"]})
    reqBodyData = json.loads(request.data.decode())
    if "Ticker" in reqBodyData and IsAuthentic(reqBodyData):
      criticalStockResult = GetCriticalStockInformation(reqBodyData["Ticker"])
      return json.dumps(criticalStockResult)
    else: 
      return json.dumps({"Valid": False,"Messages": ["Ticker not in body/not valid"]}) 
 
  except Exception as e: 
    return json.dumps({"Valid": False,"Messages": [str(e)]}) 
    
  return json.dumps({"Valid": False}) 


   

if __name__ == '__main__':
   stockSymbolNames = d.GetCachedTickerSymbols()
   api.run(host="0.0.0.0",port=7002)
