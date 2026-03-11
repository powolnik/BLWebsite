"""
BLACK LIGHT Collective — Scene Builder 3D / Serializers
Serializery edytora scen 3D: kategorie modeli, modele (odczyt i upload),
sceny (lista, detal, zapis z obsługą danych binarnych base64).
"""
import base64

from rest_framework import serializers

from .models import Model3D, Model3DCategory, Scene


class Model3DCategorySerializer(serializers.ModelSerializer):
    """Serializer kategorii modeli 3D."""
    class Meta:
        model = Model3DCategory
        fields = '__all__'


class Model3DSerializer(serializers.ModelSerializer):
    """Serializer modelu 3D z pełnym URL do pliku (read-only)."""
    category = Model3DCategorySerializer(read_only=True)
    model_file_url = serializers.SerializerMethodField()

    class Meta:
        model = Model3D
        fields = [
            'id', 'category', 'name', 'slug', 'description',
            'model_file', 'model_file_url', 'thumbnail',
            'bbox_width', 'bbox_height', 'bbox_depth',
            'weight', 'max_instances', 'price_per_unit',
            'power_consumption', 'is_active',
            'created_at', 'updated_at',
        ]

    def get_model_file_url(self, obj):
        """Buduje absolutny URL do pliku modelu 3D."""
        request = self.context.get('request')
        if obj.model_file and request:
            return request.build_absolute_uri(obj.model_file.url)
        return None


class Model3DUploadSerializer(serializers.ModelSerializer):
    """Serializer do uploadu modeli 3D przez admina."""
    class Meta:
        model = Model3D
        fields = [
            'id', 'category', 'name', 'slug', 'description',
            'model_file', 'thumbnail',
            'bbox_width', 'bbox_height', 'bbox_depth',
            'weight', 'max_instances', 'price_per_unit',
            'power_consumption', 'is_active',
        ]


class SceneListSerializer(serializers.ModelSerializer):
    """Skrócony serializer sceny do widoku listy."""
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Scene
        fields = [
            'id', 'name', 'slug', 'user', 'thumbnail',
            'is_public', 'created_at', 'updated_at',
        ]


class SceneDetailSerializer(serializers.ModelSerializer):
    """Pełny detal sceny — scene_json, ale NIE surowe dane binarne.

    Pole has_binary informuje klienta, czy dostępny jest eksport BL3D.
    """
    user = serializers.StringRelatedField(read_only=True)
    has_binary = serializers.SerializerMethodField()

    class Meta:
        model = Scene
        fields = [
            'id', 'name', 'slug', 'user', 'description',
            'grid_width', 'grid_height', 'grid_depth',
            'scene_json', 'has_binary', 'thumbnail',
            'is_public', 'created_at', 'updated_at',
        ]

    def get_has_binary(self, obj):
        """Sprawdza, czy scena ma dane binarne BL3D."""
        return obj.scene_data is not None and len(obj.scene_data) > 0


class SceneSaveSerializer(serializers.ModelSerializer):
    """Serializer zapisu scen — przyjmuje dane binarne jako base64.

    Pole scene_data_base64 jest write-only i konwertowane na bytes
    przed zapisem do BinaryField.
    """
    scene_data_base64 = serializers.CharField(
        write_only=True, required=False, allow_blank=True,
        help_text='Base64-encoded BL3D binary data',
    )

    class Meta:
        model = Scene
        fields = [
            'id', 'name', 'slug', 'description',
            'grid_width', 'grid_height', 'grid_depth',
            'scene_json', 'scene_data_base64', 'thumbnail',
            'is_public',
        ]

    def validate_scene_data_base64(self, value):
        """Dekoduje base64 na bytes; zwraca None dla pustych danych."""
        if value:
            try:
                return base64.b64decode(value)
            except Exception:
                raise serializers.ValidationError('Invalid base64-encoded data.')
        return None

    def create(self, validated_data):
        """Wyciąga zdekodowane dane binarne i zapisuje do scene_data."""
        binary_data = validated_data.pop('scene_data_base64', None)
        if binary_data is not None:
            validated_data['scene_data'] = binary_data
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Aktualizuje dane binarne sceny (jeśli przesłane)."""
        binary_data = validated_data.pop('scene_data_base64', None)
        if binary_data is not None:
            validated_data['scene_data'] = binary_data
        return super().update(instance, validated_data)
