import os

import psycopg2
from dotenv import load_dotenv


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

load_dotenv(
    os.path.join(PROJECT_ROOT, ".env"),
    encoding="utf-8"
)


def get_connection():

    host = os.getenv("POSTGRES_CONN_HOST")
    port = os.getenv("POSTGRES_CONN_PORT")
    database = os.getenv("ELT_DATABASE_NAME")
    user = os.getenv("ELT_DATABASE_USERNAME")
    password = os.getenv("ELT_DATABASE_PASSWORD")

    print("PostgreSQL connection:")
    print(f"host={host}")
    print(f"port={port}")
    print(f"database={database}")
    print(f"user={user}")

    return psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )