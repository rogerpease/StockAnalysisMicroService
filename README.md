# StockAnalysis

This is meant a simple demonstration of Microservices. 
There is no intent to recommend or discourage purchase of any particular stock nor am I offering to buy or sell stocks.
If I had a brilliant scheme for buying stocks I wouldn't put it here. :)

I didn't have time to make this fully secure. 
If I did of course I would have pursued: 
   * Authorization and Authentication. 
   * Input scrubbing 
   * Wrapping Sockets with TLS
   * Not passing secrets via environment variables. 
   
However:
   * There is no storage of critical information. All the information is publically available.  
   * I don't want to accidentally give away my company's procedures.
   * There is very little input.

# Microservices 

The following microservices are created: 

1 StockTickerMicroService- Keeps a list of tickers we can look at. 
1 StockFetchMicroService- Queries a database of stocks and keeps in a local cache. 
1 StockQuoteMicroService Queries the database of stocks built by StockFetchMicroService 
1 StockAnalysisMicroService Analyzes stocks from StockQuoteMicroService and makes recommendations. 


# Building

make clean && make all
