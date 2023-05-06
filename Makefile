.PHONY: StockDataMicroserviceCache StockTickerMicroService StockQuoteMicroService



unused:
	@echo "make install or make clean" 

clean: 
	cd StockTickerMicroService; make clean  || true
	cd StockQuoteMicroService; make -f Makefile.StockQuoteMicroService clean  || true
	cd StockQuoteMicroService; make -f Makefile.StockFetchMicroService clean  || true
	cd StockAnalysisMicroService; make -f Makefile clean  || true
	docker volume rm StockDataMicroserviceCache || true

# If you get "end of file unexpected" here check:
#   no spaces after \ 
#   Semicolon after if command 

# Update /etc/exportfs as: /opt/nfs/StockDataCache  localhost(rw,sync)

StockDataMicroserviceCache:
	if docker volume ls | grep -q "StockDataMicroserviceCache"; \
	then echo "Cache exists"; \
	else docker volume create --driver local --opt type=nfs --opt o=addr=10.0.0.150,rw --opt device=:/opt/nfs/StockDataCache StockDataMicroserviceCache; \
	fi

StockTickerMicroService: StockDataMicroserviceCache
	@echo "Making Stock Ticker Microservice" 
	cd StockTickerMicroService; make install 

StockFetchMicroService: StockTickerMicroService
	@echo "Making Stock Fetch Microservice" 
	cd StockQuoteMicroService; make -f Makefile.StockFetchMicroService install

StockQuoteMicroService: StockFetchMicroService
	@echo "Making Stock Quote Microservice" 
	cd StockQuoteMicroService; make -f Makefile.StockQuoteMicroService install

StockAnalysisMicroService: StockQuoteMicroService
	@echo "Making Stock Analysis Microservice" 
	cd StockAnalysisMicroService; make -f Makefile install


install: StockAnalysisMicroService 
	@echo "Done"
