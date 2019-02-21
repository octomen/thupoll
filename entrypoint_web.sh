#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

echo 'create db'
python -m server.init_db
echo 'create ok'

exec gunicorn -w 4 -b 0.0.0.0:5000 "server.app_factory:init_app()"
