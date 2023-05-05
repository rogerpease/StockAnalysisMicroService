#!/usr/bin/env python3 
#
#
#
#

import os
import json 
import time
import sys 
import requests 
import random

from StockDataSet import StockDataSet

CACHED="cached" 
apiKey = os.environ["ALPHAVANTAGEAPIKEY"]

from datetime import datetime,timedelta

def DateTimeToStr(dt):
   return dt.strftime("%Y-%m-%d")


class AlphaVantageDataSet(StockDataSet):

  def __init__(self,stockCacheRootPath,maxDaysBack=31):
    StockDataSet.__init__(self,stockCacheRootPath,maxDaysBack)

  def FullFilePathAndName(self,root,dateTime): 
    return self.stockCacheRootPath+"/"+root+"_"+DateTimeToStr(dateTime)+".json"

  @staticmethod
  def FileNameRoot(sym,fn): 
    return sym+"_"+fn

  def FindCacheFile(self,fileNameRoot): 

    daysBack = 0 
    while daysBack < self.maxDaysBack: 
      date = datetime.today() - timedelta(days=daysBack)
      filename = self.FullFilePathAndName(fileNameRoot,date)

      if os.path.exists(filename):
        return filename
      daysBack += 1

    return None  


  def MakeReq(self,sym=None,fn=None,doNotFetch=False): 
  
    url = 'https://www.alphavantage.co/query?function='+fn+'&symbol='+sym+'&apikey='+apiKey

    # Search for file: 
    fileNameRoot = AlphaVantageDataSet.FileNameRoot(sym,fn)
    cachedFile = self.FindCacheFile(fileNameRoot)
  
    if cachedFile == None:
      if doNotFetch:
        return None
      try: 
        r = requests.get(url)
        data = r.json()
        if "Note" in data and len(data.keys()) == 1:
          print("CAPACITY HIT") 
          return None
    
        with open(self.FullFilePathAndName(fileNameRoot,datetime.today()),"w") as f:
          f.write(json.dumps(data))
          f.close()

      except Exception as e: 
        print("Exception ",str(e)) 
   
    else:
      with open(cachedFile,"r") as f:
        data = json.loads("".join(f.readlines()))

    return {"data": data,"cached": cachedFile != None} 


  def FetchBatch(self,symbolList):
    fetchedFromAPI = 0 
    for symbol in symbolList:
      result = self.MakeReq(sym=symbol,fn="OVERVIEW") 
      if result["cached"] == False:
        fetchedFromAPI += 1   
        time.sleep(15)
      result = self.MakeReq(sym=symbol,fn="TIME_SERIES_WEEKLY") 
      if result["cached"] == False:
        fetchedFromAPI += 1   
        time.sleep(15)


  def GetAllStockInfo(self,stockSymbolList):
    
    results = []
    for stock in stockSymbolList:
      fileNameRoot = AlphaVantageDataSet.FileNameRoot(stock,"OVERVIEW")
      fileName = self.FindCacheFile(fileNameRoot)
      if not fileName == None and os.path.exists(fileName):
        try: 
          with open(fileName,'r') as f:
            jsonText = "".join(f.readlines())
          result = {} 
          info = json.loads(jsonText)
          for field in ["Symbol","DividendYield"]:
            if field in info:
              result[field] = info[field]
            else:
              raise(Exception("Field "+field +" not found for "+fileName + jsonText)) 
          results.append(result) 
        except Exception as e:
          print(str(e))
          pass


  #
  # Get names of any cached stocks 
  # 
  def GetCachedTickerSymbols(self):
     
    stockNames = {}
    for root,dirs,fileNames in os.walk(self.stockCacheRootPath):
      for fileName in fileNames:
        stockTicker = fileName.split("_")[0]
        stockNames[stockTicker] = 1 

    return list(stockNames.keys())

def SelfTest():

  ds = AlphaVantageDataSet("./testCache") 
  cachedStockNames = ds.GetCachedTickerSymbols()
  assert "ACCD" in cachedStockNames,cachedStockNames
  assert len(cachedStockNames) > 0
  result = ds.MakeReq(sym="ACCD",fn="OVERVIEW",doNotFetch=True) 
  assert result["cached"] == True

def RunFetch(): 


  ds = AlphaVantageDataSet("/opt/nfs/StockDataCache") 
  cachedSymbols = ds.GetCachedTickerSymbols()
  ds.FetchBatch(cachedSymbols)

  try:
    snrequest = requests.get("http://localhost:7000/rest/v1/SymbolNames")
    symbolnames = snrequest.json()
  except Exception as e: 
    print("Exception when requesting SymbolNames: "+str(e))   
    exit(0) 

  random.shuffle(symbolnames)
  ds.FetchBatch(symbolNames)

if __name__ == "__main__":

  SelfTest()
