"""
BLACK LIGHT Collective — Config / Settings / Production
Ustawienia produkcyjne — rozszerzają base.py.
Konfiguracja: PostgreSQL (dj_database_url), WhiteNoise dla SPA,
zabezpieczenia cookies/SSL, statyczne pliki.
"""
import os

import dj_database_url

from .base import *  # noqa: F401,F403 — import all base settings

DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# =============================================================================
# Baza danych — PostgreSQL via DATABASE_URL
# =============================================================================
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', ''),
        conn_max_age=600,             # Persistent connections (10 min)
        conn_health_checks=True,      # Sprawdzanie zdrowia połączeń
        ssl_require=True,             # Wymagaj SSL w produkcji
    )
}

# =============================================================================
# Frontend SPA — React build serwowany przez WhiteNoise
# =============================================================================
# build.sh kopiuje frontend/dist/ → backend/frontend_dist/
FRONTEND_DIR = BASE_DIR / 'frontend_dist'

# WHITENOISE_ROOT serwuje pliki z frontend_dist/ bezpośrednio w root (/)
# Dzięki temu /assets/index-xxx.js → frontend_dist/assets/index-xxx.js
# WhiteNoise obsługuje to PRZED Django URL routing — zero konfliktów z SPA catch-all
if FRONTEND_DIR.exists():
    WHITENOISE_ROOT = str(FRONTEND_DIR)

# NIE dodajemy frontend_dist do STATICFILES_DIRS — WhiteNoise Root to obsługuje
# STATICFILES_DIRS tylko dla Django's own static files
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# =============================================================================
# Bezpieczeństwo — cookies, SSL, headers
# =============================================================================
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True           # Cookies tylko po HTTPS
CSRF_COOKIE_SECURE = True              # CSRF cookie tylko po HTTPS
SECURE_SSL_REDIRECT = False            # Render/proxy obsługuje przekierowanie
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# =============================================================================
# Static files — CompressedStaticFilesStorage (BEZ Manifest)
# =============================================================================
# Vite już hashuje nazwy plików, ManifestStaticFilesStorage dodałby
# DRUGI hash i zepsuł ścieżki w index.html
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# =============================================================================
# CORS — produkcyjne originy z env
# =============================================================================
CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS', ''
).split(',') if os.environ.get('CORS_ALLOWED_ORIGINS') else []
