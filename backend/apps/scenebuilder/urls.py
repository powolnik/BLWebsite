"""
BLACK LIGHT Collective — Scene Builder 3D / URLs
Routing endpointów edytora 3D: kategorie, modele, sceny.
"""
from rest_framework.routers import DefaultRouter

from .views import Model3DCategoryViewSet, Model3DViewSet, SceneViewSet

router = DefaultRouter()
router.register(r'categories', Model3DCategoryViewSet, basename='category')
router.register(r'models', Model3DViewSet, basename='model3d')
router.register(r'scenes', SceneViewSet, basename='scene')

urlpatterns = router.urls
