"""
BLACK LIGHT Collective — Configurator / Serializers
Serializery dla szablonów scen, komponentów, kategorii,
zamówień (lista / detal / tworzenie) i elementów zamówienia.
"""
from rest_framework import serializers

from .models import SceneTemplate, ComponentCategory, Component, Order, OrderItem


class SceneTemplateSerializer(serializers.ModelSerializer):
    """Serializer szablonu sceny z dynamicznym URL obrazka."""
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = SceneTemplate
        fields = [
            'id', 'name', 'slug', 'description', 'base_price',
            'image_url', 'width', 'depth', 'height',
        ]

    def get_image_url(self, obj):
        """Deleguje do modelu — preferuje upload, fallback na zewnętrzny URL."""
        return obj.get_image_url()


class ComponentSerializer(serializers.ModelSerializer):
    """Serializer komponentu z nazwą i kolorem kategorii."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Component
        fields = [
            'id', 'name', 'slug', 'description', 'short_desc', 'price',
            'image_url', 'icon_name', 'color',
            'category', 'category_name', 'category_color',
            'width_m', 'depth_m',
            'specs', 'power_consumption', 'weight_kg',
            'is_available', 'max_quantity',
        ]

    def get_image_url(self, obj):
        """Deleguje do modelu — preferuje upload, fallback na zewnętrzny URL."""
        return obj.get_image_url()


class ComponentCategorySerializer(serializers.ModelSerializer):
    """Serializer kategorii z zagnieżdżoną listą komponentów."""
    components = ComponentSerializer(many=True, read_only=True)

    class Meta:
        model = ComponentCategory
        fields = ['id', 'name', 'slug', 'icon', 'color', 'description', 'order', 'components']


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer elementu zamówienia z danymi wizualizacyjnymi komponentu."""
    component_name = serializers.CharField(source='component.name', read_only=True)
    component_icon = serializers.CharField(source='component.icon_name', read_only=True)
    component_color = serializers.CharField(source='component.color', read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id', 'component', 'component_name', 'component_icon', 'component_color',
            'quantity', 'unit_price', 'subtotal', 'position_data', 'notes',
        ]
        read_only_fields = ['unit_price', 'subtotal']


class OrderListSerializer(serializers.ModelSerializer):
    """Skrócony serializer zamówienia do widoku listy."""
    template_name = serializers.CharField(source='template.name', read_only=True, default='')
    item_count = serializers.IntegerField(source='items.count', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'template_name', 'status', 'event_name', 'event_date',
            'event_location', 'total_price', 'item_count', 'created_at',
        ]


class OrderDetailSerializer(serializers.ModelSerializer):
    """Pełny serializer zamówienia z listą elementów i szablonem."""
    items = OrderItemSerializer(many=True, read_only=True)
    template = SceneTemplateSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'template', 'status', 'event_name', 'event_date',
            'event_end_date', 'event_location', 'expected_audience',
            'subtotal', 'template_price', 'discount', 'total_price',
            'notes', 'scene_data', 'items', 'created_at', 'updated_at',
        ]
        read_only_fields = ['subtotal', 'template_price', 'total_price']


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer tworzenia zamówienia — przyjmuje listę elementów inline."""
    items = serializers.ListField(child=serializers.DictField(), write_only=True, required=False)

    class Meta:
        model = Order
        fields = [
            'template', 'event_name', 'event_date', 'event_end_date',
            'event_location', 'expected_audience', 'notes', 'scene_data', 'items',
        ]

    def create(self, validated_data):
        """Tworzy zamówienie z elementami w jednej transakcji.

        1. Wyciąga items z danych wejściowych
        2. Przypisuje użytkownika i cenę szablonu
        3. Tworzy zamówienie i jego elementy
        4. Przelicza total
        """
        items_data = validated_data.pop('items', [])
        validated_data['user'] = self.context['request'].user
        if validated_data.get('template'):
            validated_data['template_price'] = validated_data['template'].base_price
        order = super().create(validated_data)
        # Tworzenie elementów zamówienia z cenami z chwili składania
        for item in items_data:
            comp = Component.objects.get(pk=item['component_id'])
            OrderItem.objects.create(
                order=order,
                component=comp,
                quantity=item.get('quantity', 1),
                unit_price=comp.price,
                subtotal=comp.price * item.get('quantity', 1),
                position_data=item.get('position_data', {}),
            )
        order.recalculate_total()
        return order
