from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    # JWT auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # App APIs
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/portfolio/', include('apps.portfolio.urls')),
    path('api/configurator/', include('apps.configurator.urls')),
    path('api/shop/', include('apps.shop.urls')),
]

# Media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Serwuj media z Django w produkcji (admin uploads)
    from config.views import media_serve
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', media_serve),
    ]

# SPA catch-all — MUSI być na końcu
if not settings.DEBUG:
    from config.views import spa_index
    urlpatterns += [
        re_path(r'^(?!api/|admin/|static/|media/|assets/|.*?\.[a-z0-9]{2,4}$).*$', spa_index),
    ]
