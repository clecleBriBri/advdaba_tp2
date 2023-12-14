FROM python:3.9-slim

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1

RUN pip install ijson neo4j

RUN apt-get update && apt-get install -y curl

COPY import.py .

CMD curl -s http://vmrum.isc.heia-fr.ch/dblpv13.json | sed -r 's/NumberInt\(([0-9]+)\)/\1/g' | python3 import.py
