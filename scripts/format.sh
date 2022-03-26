#!/usr/bin/env bash

set -e
set -x

black naccbis tests
find naccbis tests -name '*.py' | xargs pyupgrade --py39-plus
