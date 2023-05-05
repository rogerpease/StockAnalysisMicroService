#!/usr/bin/env python3 

from flask import Flask, json,request 
import time 
import requests
import os
from tabulate import tabulate
import sys
import threading


sortByDividendPage = ""

SHARESOUTSTANDING="SharesOutstanding" 
api = Flask(__name__)

#
#
# The super brillant algorithm that will make me rich. Just sort the stocks by dividend yield. 
#
#
#
def ByDividendYield(e):
    return e["DividendYield"]

def SortByDividend():
    try: 
      returnedStockList = [] 
      errorList         = [] 
      stockSymbolNamesResult = requests.get("http://10.0.0.150:7000/rest/v1/StockTickerSymbols").json()
      conCount = 0 
      if stockSymbolNamesResult["Valid"] == False:
          return {"Valid": False, "Messages": ["Could not get symbol List"] } 	
      stockSymbolNames = stockSymbolNamesResult["data"] 
      for stockTicker in stockSymbolNames:
        try:
          result = requests.get("http://10.0.0.150:7002/rest/v1/StockInfoByTicker",data=json.dumps({"Ticker": stockTicker})).json()
          #{'Valid': True, 'data': [{'50DayMovingAverage': '10.39', '52WeekHigh': '10.5', '52WeekLow': '9.85', 'DividendYield': '0', 'Price': 12.987849993252581, 'Ticker': 'TGAA'}]}
          print(result) 
          if "data" in result and len(result['data']) and "DividendYield" in result['data'] and result['data']["DividendYield"] != None \
                           and result['data']["DividendYield"] != "None":
            returnedStockList.append({"Ticker": stockTicker, "DividendYield": result["data"]["DividendYield"] }) 
        except Exception as e:
           errorList.append((stockTicker,e))
      returnedStockList.sort(key=ByDividendYield)   
      return {"Valid": True, "Recommendations": returnedStockList, "Errors": errorList } 	
    except Exception as e:
      return {"Valid": False, "Messages": ["Excepted out",str(conCount), str(e)]} 	


def IsAuthentic(jsonBody): 
  return True 

def IsAuthorized(jsonBody):
  return True 

@api.route('/ByDividend.html', methods=['GET'])
def getDividendPage():
    # Normally I would of course add access controls through htaccess or other web controls. 
    global sortByDividendPage 
    return "<b>THIS IS NOT A RECOMMENDATION TO BUY OR SELL STOCK!!!</b>"+"<pre>"+ sortByDividendPage + "</pre>"

 
def RunSortByDividend():
    global sortByDividendPage
    print ("Generating Page") 
    sortByDividendPage = "<b>Page being Generated</b>"
    while True: 
       try:
         sortByDividendPage_temp  = "<pre>"
         sbdResult = SortByDividend()
         print ("Sorted!") 
         if sbdResult["Valid"]:
            sbdRecommendations = sbdResult["Recommendations"]
            print(sbdRecommendations) 
            print ("Reversing!") 
            reverselist = list(reversed(sbdRecommendations))
            for stock in reverselist:
              sortByDividendPage_temp += stock["Ticker"] + " " + str(stock["DividendYield"]) + "\n"

            errorList = sbdResult["Errors"]
            for error in errorList:
              sortByDividendPage_temp += str(error) + "\n"
         else:
              sortByDividendPage_temp += 'Could not generate page: '+str(sbdResult)
         sortByDividendPage_temp  += "</pre>"
         sortByDividendPage  = sortByDividendPage_temp

       except Exception as e: 
         sortByDividendPage = "RunSortByDividend Excepted out. Normally I would cache this and print a hashed error code so an internal user could debug. "+str(e)
         print ("RunSortByDividend Excepted out. Normally I would cache this and print a hashed error code so an internal user could debug. "+str(e))
       finally: 
         # Wait a day and regerate. 
         time.sleep(3600*24) 

if __name__ == '__main__':
   print ("Starting Daemon.. Now serving  /ByDividend.html") 
   # Run on both loopback and home networks. 
   # For a larger program I'd of course monitor thread progress and add watchdogs/etc. 
   sbdThread = threading.Thread(target=RunSortByDividend,args=())
   sbdThread.start()
   api.run(host="0.0.0.0",port=7003)
   
