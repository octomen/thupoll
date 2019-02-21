#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

exec gunicorn -w 4 -b 0.0.0.0:5000 "server.app_factory:init_app()"
