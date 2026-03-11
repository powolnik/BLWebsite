"""
BLACK LIGHT Collective — Notifications / Admin
Panel administracyjny powiadomień i logów emaili.
"""
from django.contrib import admin

from .models import Notification, EmailLog


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Panel admina powiadomień z filtrami typu i statusu przeczytania."""
    list_display = ['title', 'user', 'type', 'is_read', 'created_at']
    list_filter = ['type', 'is_read']
    search_fields = ['title', 'message']


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    """Panel admina logów emaili z filtrem statusu."""
    list_display = ['subject', 'recipient', 'status', 'sent_at']
    list_filter = ['status']
