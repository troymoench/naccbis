FROM python:3.9-slim-bullseye

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY setup.py /app
# COPY conf.py /app

COPY ./docker/start_api.sh /start_api.sh
RUN chmod +x /start_api.sh

COPY ./docker/gunicorn_conf.py /app/gunicorn_conf.py

COPY naccbis/ /app/naccbis/
COPY webapp/ /app/webapp/
RUN python setup.py install
# only for django
WORKDIR /app/webapp
