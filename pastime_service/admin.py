from django.contrib import admin
from .models import Event, APIKey

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('organizer', 'event_name', 'event_description')

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('key_description',)
