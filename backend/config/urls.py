"""
BLACK LIGHT Collective — URLs
Routing: admin, JWT, API apps, health check, SPA catch-all.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import spa_index, media_serve


def health_check(request):
    """Health check endpoint for Render."""
    return JsonResponse({"status": "ok"})


urlpatterns = [
    # Health check (Render pings this)
    path('health/', health_check, name='health'),

    # Admin
    path('admin/', admin.site.urls),

    # JWT Auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API apps
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/portfolio/', include('apps.portfolio.urls')),
    path('api/shop/', include('apps.shop.urls')),
    path('api/scene-builder/', include('apps.scenebuilder.urls')),

    # Media files (production)
    re_path(r'^media/(?P<path>.*)$', media_serve, name='media'),
]

# Dev: serve media via Django
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# =====================================================================
# SPA Catch-All — MUST be last!
# Every path not caught by API/admin/static/media goes to React.
# =====================================================================
urlpatterns += [
    re_path(r'^(?!api/|admin/|static/|media/|health/).*$', spa_index, name='spa'),
]
