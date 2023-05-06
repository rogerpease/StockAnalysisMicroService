#!/usr/bin/env python3 

#
# This runs every day and pulls 500 stock ticks from an API. 
#  That's all I could get for free. :) 
#
#
#

from flask import Flask, json
import time 
from datetime import datetime 
import requests
import random  
from threading import Thread
import os
import sys
sys.path.append("StockDataSets") 

from AlphaVantageDataSet import AlphaVantageDataSet

stockSymbolNames = [] 

alphaVantageCacheMountPoint = os.environ["STOCKMICROSERVICEALPHAVANTAGECACHEDIR"]

dataSet = AlphaVantageDataSet(alphaVantageCacheMountPoint)

SHARESOUTSTANDING="SharesOutstanding" 
api = Flask(__name__)

myLogLines = [] 

#
# In a "real" kubernetes enironment service I'd have an ID and this sent to a centralized logger. 
#
def Log(string):
  global myLogLines
  logLine = datetime.now().strftime("%y-%M-%d %H:%M:%s")+" "+string 
  print(logLine) 
  myLogLines.append(datetime.now().strftime("%y-%M-%d %H:%M:%s")+" "+string) 
  while len(myLogLines) > 200000:
    myLogLines = myLogLines[1:]

#
# Just print out Log Lines.
#
@api.route('/Log', methods=['GET'])
def get_logs():
  global myLogLines
  return "\n".join(myLogLines)+ "\n" 



#
# Make a request from another microservice. 
#
#
def FetchStockOverviewAndTimeSeries():
  while True: 
    # Just in case new symbols come out.
    tickerSymbols = [] 
    while 0 == len(tickerSymbols): 
      try: 
        # Obviously in a production system I wouldn't hard code IPs or paths. 
        tickerSymbolResult = requests.get("http://10.0.0.150:7000/rest/v1/StockTickerSymbols") 
        if (tickerSymbolResult.status_code != 200):
          Log("Unable to get SymbolNames HTTP response code  " + str(tickerSymbolResult.status_code) + " " + tickerSymbolData)

        tickerSymbolData = tickerSymbolResult.json()
        if "Valid" in tickerSymbolData and tickerSymbolData["Valid"] and "data" in tickerSymbolData:
          tickerSymbols = list(tickerSymbolData["data"])
        else:
          raise (Exception("Error getting symbols") + str(tickerSymbolData))
      except Exception as e:
        Log("Get Ticker Symbols section- Unable to request SymbolNames " + str(e))
      finally:
        time.sleep(1)


    try: 
      random.shuffle(tickerSymbols)
      index = 0
      fetched = 0
      maxFetch = 500
      startTime = time.time() 

      while fetched < maxFetch and index < len(tickerSymbols):
        symbol = tickerSymbols[index]
         
        result = dataSet.MakeReq(sym=symbol,fn="OVERVIEW",doNotFetch=False)
        resultText = json.dumps(result) 
        if len(resultText) > 90:
          resultText = resultText[0:80]+"..." 
        Log("Symbol "+ symbol + " " + resultText )
        if result["cached"] == False:
          fetched += 1  
          time.sleep(20) 
    
        result = dataSet.MakeReq(sym=symbol,fn="TIME_SERIES_WEEKLY",doNotFetch=False)
        resultText = json.dumps(result) 
        if len(resultText) > 90:
          resultText = resultText[0:80]+"..." 
        Log("Symbol "+ symbol + " " + resultText )
        if result["cached"] == False:
          fetched += 1  
          time.sleep(20) 

        index += 1  
     
 
      endTime = time.time() 
      sleepTime = 3600*24-(endTime-startTime)
      Log("Sleeping for "+str(sleepTime)+" seconds") 
      time.sleep(3600*24-(endTime-startTime))
    except Exception as e:
      Log("Exception encountered Fetching Stock data " + str(e))
      time.sleep(10)    


if __name__ == '__main__':
   Log("Started") 
   acquireThread = Thread(target=FetchStockOverviewAndTimeSeries)
   acquireThread.start()
   apiThread = Thread(target=api.run,kwargs={"host": "0.0.0.0","port": "7001"})
   apiThread.start() 
   for t in [acquireThread,apiThread]:
      t.join()
