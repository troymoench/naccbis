#! /usr/bin/env sh
set -e
exec gunicorn -c /app/gunicorn_conf.py naccbis.api.main:app
