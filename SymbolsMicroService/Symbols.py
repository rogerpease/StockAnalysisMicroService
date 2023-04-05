#!/usr/bin/env python3 



class Symbols():
  def __init__(self, listingPath):
    self.listingPath = listingPath         

  def SymbolsList(self):
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

    return (result) 
 
if __name__ == "__main__":
  d = Symbols(".")
  print(d.SymbolsList())
