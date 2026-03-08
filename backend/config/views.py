"""
Catch-all view dla React Single Page Application.
Każdy URL który nie pasuje do /api/ ani /admin/ serwuje index.html z React builda.
React Router obsługuje routing po stronie klienta.
"""
import os
from django.http import HttpResponse
from django.conf import settings


def spa_index(request):
    """Serwuj React index.html dla wszystkich non-API routes."""
    index_path = os.path.join(settings.BASE_DIR, 'frontend_dist', 'index.html')
    try:
        with open(index_path, 'r') as f:
            return HttpResponse(f.read(), content_type='text/html')
    except FileNotFoundError:
        return HttpResponse(
            '<h1>Frontend nie jest zbudowany</h1>'
            '<p>Uruchom build.sh aby zbudować frontend</p>',
            content_type='text/html',
            status=503,
        )
