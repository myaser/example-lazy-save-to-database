#!/usr/bin/env bash

set -o errexit
set -o pipefail

# set -o nounset


cmd="$@"

# the official postgres image uses 'postgres' as default user if not set explictly.
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
exec $cmd