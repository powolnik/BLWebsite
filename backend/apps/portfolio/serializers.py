from rest_framework import serializers
from .models import TeamMember, Festival, Project, ProjectImage, Testimonial


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = [
            'id', 'name', 'role', 'bio', 'photo',
            'email', 'instagram', 'linkedin', 'behance', 'order',
        ]


class FestivalSerializer(serializers.ModelSerializer):
    project_count = serializers.IntegerField(source='projects.count', read_only=True)

    class Meta:
        model = Festival
        fields = ['id', 'name', 'location', 'website', 'logo', 'description', 'project_count']


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'image', 'caption', 'is_cover', 'order']


class ProjectListSerializer(serializers.ModelSerializer):
    """Skrocony serializer do listy projektow."""
    festival_name = serializers.CharField(source='festival.name', read_only=True, default='')
    cover_image = serializers.ImageField(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'short_description', 'festival_name',
            'date', 'category', 'is_featured', 'cover_image',
        ]


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Pelny serializer z galeria i opiniami."""
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
        qs = obj.testimonials.filter(is_visible=True)
        return TestimonialSerializer(qs, many=True).data


class TestimonialSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='project.title', read_only=True, default='')

    class Meta:
        model = Testimonial
        fields = ['id', 'author', 'role', 'content', 'avatar', 'project_title', 'rating', 'created_at']
