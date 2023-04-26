
.PHONY: clean docker dockerrun dockerinstall

#
# Makefile Gotcha: I accidentally had a space after the ) in MSEXISTS. That made even the empty case evaluate to " " (nothing from shell cmd)+" " 
#

IMAGENAME   = stocktickermicroserviceimage
IMAGEEXISTS = $(shell docker images ls | grep ${IMAGENAME} )
MSNAME      = stocktickermicroservice
MSEXISTS    = $(shell docker ps | grep ${MSNAME} )

clean:
	docker rm -f ${MSNAME} || true
	docker rmi -f ${IMAGENAME} || true 

docker:
	echo "IMAGEEXISTS*${IMAGEEXISTS}*" 
ifeq ("${IMAGEEXISTS}","")
	docker build -t ${IMAGENAME} .
else
	echo "Image exists" 
endif 

run: docker 
	docker run --rm -e FLASK_APP=StockTickerMicroService.py -e FLASK_ENV=development  --name ${MSNAME} -p 7000:7000 ${IMAGENAME}

install:  docker
ifeq ("${MSEXISTS}","") 
	docker run -d -e FLASK_APP=StockTickerMicroService.py -e FLASK_ENV=development  --name ${MSNAME} --restart unless-stopped -p 7000:7000 ${IMAGENAME} 
else 
	echo "Service exists" 
endif
	sleep 5
	./TestRequest.py

