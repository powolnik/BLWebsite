from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/portfolio/', include('apps.portfolio.urls')),
    path('api/configurator/', include('apps.configurator.urls')),
    path('api/shop/', include('apps.shop.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# SPA catch-all — MUSI być na końcu!
# Wszystko co nie jest /api/, /admin/, /static/ trafia do React Router
if not settings.DEBUG:
    from config.views import spa_index
    urlpatterns += [
        re_path(r'^(?!api/|admin/|static/|media/).*$', spa_index),
    ]
