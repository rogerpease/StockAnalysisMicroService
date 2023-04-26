#!/usr/bin/env python3 

import re


class StockTickerSymbols():
  def __init__(self, listingPath):
    self.listingPath = listingPath         

  def SymbolsList(self):
    try:
      result = list() 
      with open(self.listingPath+"/nasdaqlisted.txt","r") as f:
        lines = f.readlines()    

      lines = lines[1:]
      lines.pop()  
      for line in lines:  
        res = line.split('|')[0] 
        result.append(res) 

      with open(self.listingPath+"/nyse-listed_csv.csv","r") as f:
        lines = f.readlines()    
      for line in lines:  
        res = line.split(',')[0] 
        result.append(res) 

      result = [x for x in result if re.match("^[A-Z]+$",x)] 
      return True, result
    except Exception as e: 
      return False, "StockTickerSymbols " + str(e)  
 
if __name__ == "__main__":
  d = StockTickerSymbols(".")
  print(d.SymbolsList())
