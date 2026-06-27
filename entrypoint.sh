#!/bin/sh

echo "Running database migrations..."
flask db upgrade

echo "Starting server..."
exec waitress-serve --host=0.0.0.0 --port=4000 app:app