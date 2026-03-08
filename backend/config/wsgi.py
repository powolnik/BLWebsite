import os
from django.core.wsgi import get_wsgi_application

# Na Render: ustaw DJANGO_SETTINGS_MODULE=config.settings.prod w Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 
    os.environ.get('DJANGO_SETTINGS_MODULE', 'config.settings.prod'))
application = get_wsgi_application()
