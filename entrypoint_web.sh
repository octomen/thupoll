#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

echo 'run migrations...'
cd server ; flask db upgrade ; cd -
echo 'migrations ok'

exec gunicorn -w 4 -b 0.0.0.0:5000 --access-logfile - --error-logfile - "server.app_factory:init_app()"
