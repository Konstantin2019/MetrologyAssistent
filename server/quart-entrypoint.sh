#!/bin/sh

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "db" -U "postgres" -c '\q'
do
  echo "Postgres is unavailable..."
  sleep 1
done

echo "Postgres is ready!"

hypercorn --bind 0.0.0.0:3001 runner:api