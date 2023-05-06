
CONTAINERNAME=stockanalysismicroservice 
IMAGENAME=stockanalysismicroserviceimage

MSNAME      = stockanalysismicroservice
MSEXISTS    = $(shell docker ps | grep ${MSNAME} )

ENVIRONMENT=-e STOCKMICROSERVICEALPHAVANTAGECACHEDIR=$(STOCKMICROSERVICEALPHAVANTAGECACHEDIR) -e ALPHAVANTAGEAPIKEY=$(ALPHAVANTAGEAPIKEY)

.PHONY: clean run install 

clean:
	docker stop $(CONTAINERNAME)  || true 
	docker rm $(CONTAINERNAME)  || true 
	docker rmi $(IMAGENAME)  || true 


IMAGEINDOCKER := $(shell docker image ls | grep "$(IMAGENAME)")

dockerbuild:
	@echo "Image In Docker: ${IMAGEINDOCKER}"
ifeq ("${IMAGE}", "") 
	docker build -t $(IMAGENAME) -f Dockerfile .
endif

run: dockerbuild
	docker run --rm -it $(ENVIRONMENT) --name $(CONTAINERNAME) --mount source=StockDataMicroserviceCache,target=/opt/nfs/StockDataCache -p 7003:7003 $(IMAGENAME)

install: dockerbuild 
ifeq ("${MSEXISTS}","")
	docker run -d -it $(ENVIRONMENT) --name $(CONTAINERNAME) --mount source=StockDataMicroserviceCache,target=/opt/nfs/StockDataCache -p 7003:7003 --restart unless-stopped  $(IMAGENAME)
else
	echo "Service exists"
endif
	echo "This will take a bit to compile all the data" 
	sleep 30
	./Test.StockAnalysisMicroService.py

