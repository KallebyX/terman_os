#!/bin/bash

set -e

host="db"
port="5432"
user="$POSTGRES_USER"
password="$POSTGRES_PASSWORD"
database="$POSTGRES_DB"

until PGPASSWORD=$password psql -h "$host" -p "$port" -U "$user" -d "$database" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec "$@"