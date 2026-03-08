from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('team', views.TeamMemberViewSet, basename='team')
router.register('festivals', views.FestivalViewSet, basename='festival')
router.register('projects', views.ProjectViewSet, basename='project')
router.register('testimonials', views.TestimonialViewSet, basename='testimonial')

urlpatterns = [
    path('', include(router.urls)),
]
