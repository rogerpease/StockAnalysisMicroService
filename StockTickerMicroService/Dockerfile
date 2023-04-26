FROM python:3.8-slim-buster

WORKDIR /python
COPY . /python 
RUN pip3 install flask
RUN chmod 755 /python/*.py
EXPOSE 7000 
CMD ["/python/StockTickerMicroService.py"]
