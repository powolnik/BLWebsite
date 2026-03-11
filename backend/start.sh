#!/usr/bin/env bash
# BLACK LIGHT Collective — Start Script (Render)
set -o errexit

# --- Krok 1: Migracje bazy danych ---
echo "=== Running migrations ==="
python manage.py migrate --noinput

# --- Krok 2: Seed data (jeśli baza pusta) ---
echo "=== Loading seed data ==="
python manage.py seed_data 2>/dev/null || echo "Seed already loaded or skipped"

# --- Krok 3: Gunicorn z optymalnymi ustawieniami dla Render ---
echo "=== Starting Gunicorn ==="
exec gunicorn config.wsgi:application \
    --bind "0.0.0.0:${PORT:-10000}" \
    --workers 2 \
    --threads 2 \
    --timeout 120 \
    --preload \
    --access-logfile - \
    --error-logfile - \
    --log-level info
