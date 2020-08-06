FROM python:3.7-buster

WORKDIR /app

RUN pip install pipenv
COPY Pipfile* ./
RUN pipenv lock -r > requirements.txt
RUN pip install -r requirements.txt
COPY setup.py /app
COPY conf.py /app
COPY naccbis/ /app/naccbis/
COPY webapp/ /app/webapp/
RUN python setup.py install
WORKDIR /app/webapp
