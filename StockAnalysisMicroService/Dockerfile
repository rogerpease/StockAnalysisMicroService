FROM python:3.8-slim-buster

WORKDIR /python
RUN pip3 install flask
RUN pip3 install requests
RUN pip3 install tabulate
COPY . /python 
RUN chmod 755 /python/*.py
EXPOSE 7003 
CMD ["./StockAnalysisMicroService.py"]
