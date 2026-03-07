from rest_framework import serializers
from .models import SceneTemplate, ComponentCategory, Component, Order, OrderItem


class SceneTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SceneTemplate
        fields = [
            'id', 'name', 'slug', 'description', 'base_price',
            'preview_image', 'model_3d_url', 'width', 'depth', 'height',
        ]


class ComponentSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Component
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'image',
            'category', 'category_name', 'specs', 'power_consumption',
            'weight_kg', 'is_available', 'max_quantity',
        ]


class ComponentCategorySerializer(serializers.ModelSerializer):
    components = ComponentSerializer(many=True, read_only=True)

    class Meta:
        model = ComponentCategory
        fields = ['id', 'name', 'slug', 'icon', 'description', 'order', 'components']


class OrderItemSerializer(serializers.ModelSerializer):
    component_name = serializers.CharField(source='component.name', read_only=True)
    component_image = serializers.ImageField(source='component.image', read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id', 'component', 'component_name', 'component_image',
            'quantity', 'unit_price', 'subtotal', 'position_data', 'notes',
        ]
        read_only_fields = ['unit_price', 'subtotal']


class OrderListSerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(source='template.name', read_only=True, default='')
    item_count = serializers.IntegerField(source='items.count', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'template_name', 'status', 'event_name', 'event_date',
            'event_location', 'total_price', 'item_count', 'created_at',
        ]


class OrderDetailSerializer(serializers.ModelSerializer):
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
    """Serializer do tworzenia zamowienia."""
    class Meta:
        model = Order
        fields = [
            'template', 'event_name', 'event_date', 'event_end_date',
            'event_location', 'expected_audience', 'notes', 'scene_data',
        ]

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        if validated_data.get('template'):
            validated_data['template_price'] = validated_data['template'].base_price
        return super().create(validated_data)
