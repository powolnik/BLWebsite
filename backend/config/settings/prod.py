import os
import dj_database_url
from .base import *

DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# --- DATABASE ---
# Render udostępnia DATABASE_URL automatycznie po połączeniu bazy PostgreSQL
# Przykład: postgres://user:pass@host.render.com:5432/dbname
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', ''),
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True,
    )
}

# --- FRONTEND SPA: React build serwowany przez Django + WhiteNoise ---
# build.sh kopiuje frontend/dist/ → backend/frontend_dist/
FRONTEND_DIR = BASE_DIR / 'frontend_dist'
if FRONTEND_DIR.exists():
    TEMPLATES[0]['DIRS'].append(FRONTEND_DIR)
    STATICFILES_DIRS = [
        BASE_DIR / 'static',
        FRONTEND_DIR,
    ]

# --- SECURITY ---
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# WAŻNE: Render obsługuje SSL na swoim proxy — NIE włączaj SSL_REDIRECT
# bo dostaniesz nieskończoną pętlę przekierowań!
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# --- STATIC FILES ---
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# CORS — na produkcji frontend i API są na tej samej domenie
CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS', ''
).split(',') if os.environ.get('CORS_ALLOWED_ORIGINS') else []
