from django.contrib import admin
from apps.artist.models import Artist
# Register your models here.

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('stage_name', 'manager', 'artist_fields', 'contact', 'artist_charge')  # Add 'manager' to list display
    list_filter = ('artist_fields', 'manager', 'artist_charge')  # Filter by manager, artist fields, and charge
    search_fields = ('stage_name','contact')  # Add search for manager
    list_editable = ('artist_charge',)  # Make 'artist_charge' editable in the list view

    fieldsets = (
        ('Manager Information', {
            'fields': ('manager',)
        }),
        ('Basic Information', {
            'fields': ('profile_picture', 'stage_name', 'artist_fields', 'description')
        }),
        ('Contact Information', {
            'fields': ('contact', 'instagram_profile', 'spotify_link')
        }),
        ('Financial Details', {
            'fields': ('artist_charge',)
        }),
    )