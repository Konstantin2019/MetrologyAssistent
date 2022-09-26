#!/bin/sh

echo "Waiting for db initialization…"
sleep 10

gunicorn --bind 0.0.0.0:3001 runner:api