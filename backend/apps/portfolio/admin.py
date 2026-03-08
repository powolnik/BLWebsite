from django.contrib import admin
from django.utils.html import format_html
from .models import TeamMember, Festival, Project, ProjectImage, Testimonial


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 3
    fields = ['image', 'image_preview', 'caption', 'is_cover', 'order']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:80px; border-radius:4px;" />',
                obj.image.url
            )
        return '—'
    image_preview.short_description = 'Podgląd'


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'photo_preview', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name', 'role']

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-height:40px; border-radius:50%;" />',
                obj.photo.url
            )
        return '—'
    photo_preview.short_description = 'Foto'


@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'logo_preview']
    search_fields = ['name', 'location']

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-height:30px;" />',
                obj.logo.url
            )
        return '—'
    logo_preview.short_description = 'Logo'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'festival', 'category', 'date', 'is_featured', 'image_count']
    list_filter = ['category', 'is_featured', 'festival']
    search_fields = ['title', 'description', 'client']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]
    date_hierarchy = 'date'
    save_on_top = True

    def image_count(self, obj):
        count = obj.images.count()
        return format_html(
            '<span style="color: {};">{} zdjęć</span>',
            '#00ff88' if count > 0 else '#ff4444',
            count
        )
    image_count.short_description = 'Zdjęcia'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['author', 'rating', 'is_visible', 'created_at']
    list_filter = ['rating', 'is_visible']
