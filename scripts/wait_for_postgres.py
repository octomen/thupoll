#!/usr/bin/env python3
import psycopg2
import sys
import time

MAX_ATTEMPTS = 30
DB_URL = sys.argv[1]

print("Now connect to Postgres")
for i in range(MAX_ATTEMPTS, 0, -1):
    try:
        psycopg2.connect(DB_URL)
        print("Connected to Postgres")
        sys.exit()
    except psycopg2.OperationalError:
        print("Waiting 1s for Postgres to load")
        time.sleep(1)

print("Could not connect to Postgres after {} attempts".format(MAX_ATTEMPTS))
sys.exit(1)
