#!/usr/bin/env bash

set -e -u


wait_for_postgres() {
    echo "Waiting for postgres..."
    ./scripts/wait_for_postgres.py $DB_URL
    echo "Postgres started"
}


init_db() {
    wait_for_postgres

    echo "Run migrations..."
    flask db upgrade
    echo "Migrations ok"
}


start_api() {
    # start server
    exec gunicorn -w 4 -b 0.0.0.0:5000 --access-logfile - --error-logfile - "thupoll.app_factory:init_app()"
}

# Start specified service
case ${SERVICE_NAME-'<empty>'} in
    api)
        init_db
        start_api
        ;;
    test)
        init_db
        bash
        ;;
    bash)
        bash
        ;;
    *)
        echo "Unknown service name ${SERVICE_NAME-<empty>}!"
        exit 1
        ;;
esac
