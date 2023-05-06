#!/usr/bin/env python3 



class StockDataSet():

  def __init__(self,stockCacheRootPath,maxDaysBack=31):
    self.stockCacheRootPath = stockCacheRootPath
    self.maxDaysBack=maxDaysBack



