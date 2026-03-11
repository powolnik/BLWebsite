"""
BLACK LIGHT Collective — Configurator / Views
Endpointy REST API konfiguratora scen: szablony, kategorie, komponenty,
zamówienia (CRUD + akcje: dodaj/usuń element, złóż zamówienie, podsumowanie mocy).
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import SceneTemplate, ComponentCategory, Component, Order
from .serializers import (
    SceneTemplateSerializer, ComponentCategorySerializer, ComponentSerializer,
    OrderListSerializer, OrderDetailSerializer, OrderCreateSerializer,
    OrderItemSerializer,
)
from .services import ConfiguratorService


class SceneTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """Lista aktywnych szablonów scen (tylko odczyt, lookup po slug)."""
    queryset = SceneTemplate.objects.filter(is_active=True)
    serializer_class = SceneTemplateSerializer
    lookup_field = 'slug'


class ComponentCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Lista kategorii komponentów z zagnieżdżonymi komponentami (bez paginacji)."""
    queryset = ComponentCategory.objects.prefetch_related('components')
    serializer_class = ComponentCategorySerializer
    pagination_class = None


class ComponentViewSet(viewsets.ReadOnlyModelViewSet):
    """Lista dostępnych komponentów z filtrowaniem po kategorii."""
    queryset = Component.objects.filter(is_available=True).select_related('category')
    serializer_class = ComponentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'is_available']


class OrderViewSet(viewsets.ModelViewSet):
    """CRUD zamówień scen z akcjami dodatkowymi.

    Akcje:
    - add_item: dodaj komponent do szkicu zamówienia
    - remove_item: usuń komponent z zamówienia
    - submit: złóż zamówienie (zmiana statusu draft → submitted)
    - power_summary: podsumowanie zużycia mocy i wagi
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Zwraca zamówienia bieżącego użytkownika z powiązanymi danymi."""
        return Order.objects.filter(
            user=self.request.user
        ).select_related('template').prefetch_related('items__component')

    def get_serializer_class(self):
        """Wybiera serializer w zależności od akcji (create / detail / list)."""
        if self.action == 'create':
            return OrderCreateSerializer
        if self.action in ('retrieve', 'update', 'partial_update'):
            return OrderDetailSerializer
        return OrderListSerializer

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        """Dodaj komponent do zamówienia (tylko szkice)."""
        order = self.get_object()
        if order.status != 'draft':
            return Response(
                {'error': 'Mozna edytowac tylko szkice.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            item = ConfiguratorService.add_item(
                order=order,
                component_id=request.data.get('component_id'),
                quantity=request.data.get('quantity', 1),
                position_data=request.data.get('position_data'),
            )
            return Response(OrderItemSerializer(item).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        """Usuń komponent z zamówienia."""
        order = self.get_object()
        ConfiguratorService.remove_item(order, request.data.get('item_id'))
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Złóż zamówienie — zmiana statusu na 'submitted'."""
        order = self.get_object()
        try:
            ConfiguratorService.submit_order(order)
            return Response({'status': 'Zamowienie zlozone.'})
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def power_summary(self, request, pk=None):
        """Podsumowanie zużycia mocy (W) i wagi (kg) zamówienia."""
        order = self.get_object()
        return Response(ConfiguratorService.calculate_power_summary(order))
