FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 python3-pip

RUN pip3 install pika influxdb_client numpy scikit-fuzzy pandas scipy packaging networkx

COPY prediction.py /scripts/prediction.py
COPY fuzzy_algorithm.py /scripts/fuzzy_algorithm.py 
COPY Mapa_das_Mares.csv /scripts/Mapa_das_Mares.csv



