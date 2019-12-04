FROM python:3.7-buster

RUN pip install argparse mysql-connector-python beautifulsoup4 requests

COPY . /usr/src/themoviepredictor

WORKDIR /usr/src/themoviepredictor

# Notre but : CMD python /usr/src/themoviepredictor/app.py movies import --api all --for 7