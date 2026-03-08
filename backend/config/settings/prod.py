import os
import dj_database_url
from .base import *

DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# --- DATABASE ---
# Render udostępnia DATABASE_URL — to jedyna zmienna potrzebna do bazy
# Przykład: postgres://user:pass@host:5432/dbname
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', ''),
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True,
    )
}

# --- SECURITY ---
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# WAŻNE: Render obsługuje SSL na swoim proxy — NIE ustawiaj SECURE_SSL_REDIRECT=True
# bo dostaniesz nieskończoną pętlę przekierowań!
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# --- STATIC FILES ---
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
