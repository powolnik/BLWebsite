"""
BLACK LIGHT Collective — Config / URLs
Główna konfiguracja routingu URL projektu Django.
Łączy panel admina, endpointy JWT, oraz API wszystkich aplikacji.
W trybie DEBUG serwuje pliki media.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Panel administracyjny Django
    path('admin/', admin.site.urls),

    # JWT Authentication — uzyskanie i odświeżenie tokena
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API aplikacji BLACK LIGHT Collective
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/portfolio/', include('apps.portfolio.urls')),
    path('api/configurator/', include('apps.configurator.urls')),
    path('api/shop/', include('apps.shop.urls')),
    path('api/scene-builder/', include('apps.scenebuilder.urls')),
]

# W trybie deweloperskim serwuj pliki media (uploady) przez Django
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
