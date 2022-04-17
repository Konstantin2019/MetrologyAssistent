#!/bin/sh

until flask db upgrade
do
    flask db migrate -m 'initial migration'
done

gunicorn --bind 0.0.0.0:3001 runner:api