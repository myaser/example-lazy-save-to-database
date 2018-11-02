#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


/usr/local/bin/gunicorn -b 0.0.0.0:5000 manage:app -w 4 --chdir=/app -t 0
