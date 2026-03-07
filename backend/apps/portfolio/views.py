from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import TeamMember, Festival, Project, Testimonial
from .serializers import (
    TeamMemberSerializer, FestivalSerializer,
    ProjectListSerializer, ProjectDetailSerializer,
    TestimonialSerializer,
)


class TeamMemberViewSet(viewsets.ReadOnlyModelViewSet):
    """API czlonkow zespolu (tylko odczyt)."""
    queryset = TeamMember.objects.filter(is_active=True)
    serializer_class = TeamMemberSerializer
    pagination_class = None


class FestivalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Festival.objects.all()
    serializer_class = FestivalSerializer
    search_fields = ['name', 'location']


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """API projektow z filtrami i wyszukiwaniem."""
    queryset = Project.objects.select_related('festival').prefetch_related('images')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_featured', 'festival']
    search_fields = ['title', 'description', 'client']
    ordering_fields = ['date', 'created_at', 'title']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProjectDetailSerializer
        return ProjectListSerializer


class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Testimonial.objects.filter(is_visible=True)
    serializer_class = TestimonialSerializer
    pagination_class = None
