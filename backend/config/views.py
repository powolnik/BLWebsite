import os
from pathlib import Path
from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse


def spa_index(request):
    """Serwuj index.html z React build dla SPA routing."""
    index_path = Path(settings.BASE_DIR) / 'frontend_dist' / 'index.html'
    if index_path.exists():
        return HttpResponse(index_path.read_text(), content_type='text/html')
    raise Http404('Frontend not built yet.')


def media_serve(request, path):
    """Serwuj pliki media w produkcji (dla admin uploads)."""
    file_path = Path(settings.MEDIA_ROOT) / path
    if file_path.exists() and file_path.is_file():
        return FileResponse(open(file_path, 'rb'))
    raise Http404('File not found.')
