#!/bin/sh
set -e

echo "Applying database migrations..."

flask db upgrade

echo "Migrations complete."

exec gunicorn -w 4 -b 0.0.0.0:4000 app:app