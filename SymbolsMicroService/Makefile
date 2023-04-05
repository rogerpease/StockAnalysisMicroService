.PHONY: clean docker dockerrun kubernetes 

clean:
	docker rm symbolsmicroservice:0.1.0 || true
	docker rmi symbolmsimage:0.1.0 || true 
	kubectl delete deployment symbolmsdep || true 
	kubectl delete service symbolmsdep || true 

docker:
	docker build -t symbolmsimage:0.1.0 .
	docker tag symbolmsimage:0.1.0 rogerpease/symbolmsimage:0.1.0 || true
	docker push rogerpease/symbolmsimage:0.1.0 || true

dockerrun: docker 
	docker run --rm -e FLASK_APP=SymbolsMicroService.py -e FLASK_ENV=development  --name symbolsmicroservice -p 7000:7000 rogerpease/symbolmsimage:0.1.0

dockerinstall: docker 
	docker run -d -e FLASK_APP=SymbolsMicroService.py -e FLASK_ENV=development  --name symbolsmicroservice --restart unless-stopped -p 7000:7000 rogerpease/symbolmsimage:0.1.0


# Kubernetes would make this a named service and distribute load. Not necessary for this minor service. 
#kubernetes: docker 
#	kubectl create deployment symbolmsdep --image=rogerpease/symbolmsimage:0.1.0
#	kubectl expose deployment symbolmsdep --type=NodePort --port=7000
