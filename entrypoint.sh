#!/bin/sh
set -e

. .venv/bin/activate

echo "Waiting for database..."
sleep 3 

echo "Initializing database..."
make init-db || echo "Database already initialized, skipping..."

echo "Creating migrations..."
make migrate

echo "Applying migrations..."
make upgrade

echo "Starting the application..."
exec make run
