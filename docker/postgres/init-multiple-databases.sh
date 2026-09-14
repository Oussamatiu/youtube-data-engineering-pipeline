#!/bin/bash

set -e

echo "Creating YouTube database..."

psql -v ON_ERROR_STOP=1 \
    --username "$POSTGRES_USER" \
    --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE youtube;
EOSQL

echo "YouTube database created successfully."