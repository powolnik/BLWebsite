"""
BLACK LIGHT Collective — Portfolio / Serializers
Serializery portfolio: zespół, festiwale, projekty (lista / detal),
galeria zdjęć projektów, opinie klientów.
"""
from rest_framework import serializers

from .models import TeamMember, Festival, Project, ProjectImage, Testimonial


class TeamMemberSerializer(serializers.ModelSerializer):
    """Serializer członka zespołu z linkami do social media."""
    class Meta:
        model = TeamMember
        fields = [
            'id', 'name', 'role', 'bio', 'photo',
            'email', 'instagram', 'linkedin', 'behance', 'order',
        ]


class FestivalSerializer(serializers.ModelSerializer):
    """Serializer festiwalu z liczbą powiązanych projektów."""
    project_count = serializers.IntegerField(source='projects.count', read_only=True)

    class Meta:
        model = Festival
        fields = ['id', 'name', 'location', 'website', 'logo', 'description', 'project_count']


class ProjectImageSerializer(serializers.ModelSerializer):
    """Serializer zdjęcia projektu."""
    class Meta:
        model = ProjectImage
        fields = ['id', 'image', 'caption', 'is_cover', 'order']


class ProjectListSerializer(serializers.ModelSerializer):
    """Skrócony serializer do listy projektów — z okładką i nazwą festiwalu."""
    festival_name = serializers.CharField(source='festival.name', read_only=True, default='')
    cover_image = serializers.ImageField(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'short_description', 'festival_name',
            'date', 'category', 'is_featured', 'cover_image',
        ]


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Pełny serializer projektu z galerią i opiniami."""
    images = ProjectImageSerializer(many=True, read_only=True)
    festival = FestivalSerializer(read_only=True)
    testimonials = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'description', 'short_description',
            'festival', 'client', 'date', 'category', 'is_featured',
            'video_url', 'technologies', 'images', 'testimonials', 'created_at',
        ]

    def get_testimonials(self, obj):
        """Zwraca tylko widoczne opinie powiązane z tym projektem."""
        qs = obj.testimonials.filter(is_visible=True)
        return TestimonialSerializer(qs, many=True).data


class TestimonialSerializer(serializers.ModelSerializer):
    """Serializer opinii klienta z tytułem powiązanego projektu."""
    project_title = serializers.CharField(source='project.title', read_only=True, default='')

    class Meta:
        model = Testimonial
        fields = ['id', 'author', 'role', 'content', 'avatar', 'project_title', 'rating', 'created_at']
