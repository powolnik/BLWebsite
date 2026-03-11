#!/usr/bin/env bash
# =============================================================================
# BLACK LIGHT Collective — Start Script
# Skrypt uruchamiania serwera (używany w Dockerfile / Render).
# Kolejność: migracje → seed data → Gunicorn.
# =============================================================================
set -o errexit  # Przerwij przy pierwszym błędzie

# --- Krok 1: Migracje bazy danych ---
echo "=== Running migrations ==="
python manage.py makemigrations --noinput 2>/dev/null || true  # Tworzenie migracji (jeśli potrzebne)
python manage.py migrate --noinput                              # Aplikacja migracji

# --- Krok 2: Załadowanie danych początkowych (seed) ---
echo "=== Loading seed data ==="
python manage.py seed_data 2>/dev/null || echo "Seed already loaded or skipped"

# --- Krok 3: Uruchomienie serwera Gunicorn ---
# exec zastępuje proces bash — sygnały (SIGTERM) trafiają bezpośrednio do Gunicorn
echo "=== Starting Gunicorn ==="
exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
