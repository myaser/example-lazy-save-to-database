#!/usr/bin/env bash

set -o errexit
set -o pipefail

# set -o nounset
cmd="$@"

export REDIS_URL="redis://:$REDIS_PASSWORD@redis:6379/0"
if [ -z "$RQ_REDIS_URL" ]; then
    export RQ_REDIS_URL=$REDIS_URL
fi
export FLASK_APP=manage.py
if [ -z "$POSTGRES_USER" ]; then
    export POSTGRES_USER=postgres
fi
if [ -z "$POSTGRES_PORT" ]; then
    export POSTGRES_PORT=5432
fi
export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
function postgres_ready(){
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname="$POSTGRES_DB", user="$POSTGRES_USER", password="$POSTGRES_PASSWORD", host="$POSTGRES_HOST")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}
until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
>&2 echo "Postgres is up - continuing..."


if [ -z "$cmd" ]; then
    exec /app/gunicorn.sh
else
exec $cmd
fi
