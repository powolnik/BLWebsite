import os
from django.core.wsgi import get_wsgi_application

# Render: DJANGO_SETTINGS_MODULE jest ustawiony w Environment Variables
# Domyślnie: prod (bo wsgi.py jest używany tylko na serwerze)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')
application = get_wsgi_application()
