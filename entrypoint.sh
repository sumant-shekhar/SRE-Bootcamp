set -e

echo "Applying database migrations..."
flask db upgrade || true

echo "Starting application..."
exec python app.py