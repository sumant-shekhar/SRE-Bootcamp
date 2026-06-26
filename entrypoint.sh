#!/bin/sh
set -e

echo "Applying database migrations..."
flask db upgrade
echo "Migrations complete."

echo "Starting Waitress..."
exec waitress-serve --host=0.0.0.0 --port=${PORT:-4000} app:app