from django.contrib import admin
from django.utils.html import format_html
from apps.events.models import Event

# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'event_date', 'event_start_time', 'event_end_time', 'event_status', 'display_event_image')
    list_filter = ('event_status', 'event_date', 'venue')
    search_fields = ('event_name', 'event_organizer_name', 'artist__name', 'venue__name')
    ordering = ('-event_date',)
    filter_horizontal = ('required_thing',)  # For ManyToMany field selection
    fieldsets = (
        ("Event Details", {
            'fields': ('event_name', 'event_image', 'display_event_image', 'event_description', 'event_status')
        }),
        ("Organizer Details", {
            'fields': ('manager', 'event_organizer_name', 'event_organizer_contact')
        }),
        ("Event Timing & Venue", {
            'fields': ('event_date', 'event_day_of_week', 'event_start_time', 'event_end_time', 'venue')
        }),
        ("Artists & Requirements", {
            'fields': ('artist', 'required_thing')
        }),
    )
    readonly_fields = ('display_event_image',)

    def display_event_image(self, obj):
        """Display event image in the admin panel."""
        if obj.event_image:
            return format_html('<img src="{}" width="100" height="100" style="border-radius: 5px;"/>', obj.event_image.url)
        return "No Image"
    
    display_event_image.short_description = "Event Image"

admin.site.register(Event, EventAdmin)