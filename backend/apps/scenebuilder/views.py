"""
BLACK LIGHT Collective — Scene Builder 3D / Views
Endpointy REST API edytora scen 3D: kategorie modeli, modele 3D (CRUD),
sceny użytkowników (CRUD + eksport binarny).
"""
from django.db.models import Q
from django.http import HttpResponse
from rest_framework import parsers, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Model3D, Model3DCategory, Scene
from .serializers import (
    Model3DCategorySerializer,
    Model3DSerializer,
    Model3DUploadSerializer,
    SceneDetailSerializer,
    SceneListSerializer,
    SceneSaveSerializer,
)


class Model3DCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Lista i detal kategorii modeli 3D (publiczny, tylko odczyt)."""
    queryset = Model3DCategory.objects.all()
    serializer_class = Model3DCategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class Model3DViewSet(viewsets.ModelViewSet):
    """Biblioteka modeli 3D.

    - list/retrieve: publiczny dostęp (AllowAny)
    - create/update/delete: tylko admin
    - upload_model: dedykowany endpoint do uploadu plików multipart
    """
    queryset = Model3D.objects.filter(is_active=True).select_related('category')
    serializer_class = Model3DSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        """Publiczny odczyt, admin do zapisu."""
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_serializer_class(self):
        """Upload serializer dla operacji zapisu, standardowy dla odczytu."""
        if self.action in ['create', 'update', 'partial_update', 'upload_model']:
            return Model3DUploadSerializer
        return Model3DSerializer

    @action(
        detail=False,
        methods=['post'],
        url_path='upload',
        parser_classes=[parsers.MultiPartParser, parsers.FormParser],
        permission_classes=[permissions.IsAdminUser],
    )
    def upload_model(self, request):
        """Upload nowego modelu 3D z danymi multipart/form-data."""
        serializer = Model3DUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SceneViewSet(viewsets.ModelViewSet):
    """Sceny użytkowników.

    - list: publiczne sceny + własne sceny zalogowanego użytkownika
    - CRUD: standardowe operacje
    - export-binary: pobranie danych BL3D jako pliku
    """
    serializer_class = SceneDetailSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Filtruje sceny: publiczne + własne użytkownika (na liście)."""
        qs = Scene.objects.all()
        user = self.request.user

        if self.action == 'list':
            if user.is_authenticated:
                # Pokaż sceny publiczne oraz własne sceny użytkownika
                qs = qs.filter(Q(is_public=True) | Q(user=user))
            else:
                qs = qs.filter(is_public=True)

        return qs.select_related('user')

    def get_serializer_class(self):
        """Lista → skrócony; zapis → SceneSave; detal → pełny."""
        if self.action == 'list':
            return SceneListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return SceneSaveSerializer
        return SceneDetailSerializer

    def perform_create(self, serializer):
        """Przypisuje użytkownika do sceny (jeśli zalogowany)."""
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()

    @action(detail=True, methods=['get'], url_path='export-binary')
    def export_binary(self, request, slug=None):
        """Pobierz dane binarne sceny (format BL3D) jako plik."""
        scene = self.get_object()
        if not scene.scene_data:
            return Response(
                {'detail': 'No binary data available for this scene.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        response = HttpResponse(
            bytes(scene.scene_data),
            content_type='application/octet-stream',
        )
        response['Content-Disposition'] = (
            f'attachment; filename="{scene.slug}.bl3d"'
        )
        return response
