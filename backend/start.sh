#!/usr/bin/env bash
set -o errexit

echo "=== Running migrations ==="
python manage.py makemigrations --noinput 2>/dev/null || true
python manage.py migrate --noinput

echo "=== Loading seed data ==="
python manage.py seed_data 2>/dev/null || echo "Seed already loaded or skipped"

echo "=== Starting Gunicorn ==="
exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
