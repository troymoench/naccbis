#!/usr/bin/env bash

set -e
set -x

black naccbis tests --check
isort naccbis tests --check
flake8 naccbis tests --statistics
mypy naccbis tests
