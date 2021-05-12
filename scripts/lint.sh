#!/usr/bin/env bash

set -e
set -x

mypy naccbis
flake8 naccbis tests --statistics
black naccbis tests --check
