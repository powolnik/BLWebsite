"""
BLACK LIGHT Collective — Config / Views
Widoki pomocnicze: serwowanie SPA (React index.html) oraz plików media.
Używane w produkcji, gdzie WhiteNoise serwuje static,
a te widoki obsługują SPA catch-all i media uploads.
"""
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse


def spa_index(request):
    """Serwuj index.html z React build dla SPA routing.

    Każda ścieżka niezłapana przez API/admin trafia tutaj,
    a React Router obsługuje routing po stronie klienta.
    """
    index_path = Path(settings.BASE_DIR) / 'frontend_dist' / 'index.html'
    if index_path.exists():
        return HttpResponse(index_path.read_text(), content_type='text/html')
    raise Http404('Frontend not built yet.')


def media_serve(request, path):
    """Serwuj pliki media w produkcji (dla admin uploads).

    W dev Django obsługuje to automatycznie (static(MEDIA_URL, ...)),
    ale w produkcji potrzebny jest dedykowany widok.
    """
    file_path = Path(settings.MEDIA_ROOT) / path
    if file_path.exists() and file_path.is_file():
        return FileResponse(open(file_path, 'rb'))
    raise Http404('File not found.')
