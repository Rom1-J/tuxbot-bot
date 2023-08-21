import os
import sys
import time

import psycopg2


suggest_unrecoverable_after = 10
start = time.time()


def test() -> None:
    while True:
        try:
            psycopg2.connect(
                dbname=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                host=os.getenv("POSTGRES_HOST"),
                port=os.getenv("POSTGRES_PORT"),
            )
            break

        except psycopg2.OperationalError as error:
            sys.stderr.write("Waiting for PostgreSQL to become available...\n")
            if time.time() - start > suggest_unrecoverable_after:
                sys.stderr.write(
                    "  This is taking longer than expected. "
                    "The following exception may be indicative of an "
                    f"unrecoverable error: '{error}'\n"
                )
        time.sleep(1)
