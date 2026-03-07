from django.contrib import admin
from .models import TeamMember, Festival, Project, ProjectImage, Testimonial


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name', 'role']


@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    list_display = ['name', 'location']
    search_fields = ['name', 'location']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'festival', 'category', 'date', 'is_featured']
    list_filter = ['category', 'is_featured', 'festival']
    search_fields = ['title', 'description', 'client']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]
    date_hierarchy = 'date'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['author', 'rating', 'is_visible', 'created_at']
    list_filter = ['rating', 'is_visible']
