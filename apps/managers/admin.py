from django.contrib import admin
from apps.managers.models import Manager, ManagerProfileInfo,Venue, RequiredThing


# Register your models here.
admin.site.register(Manager)
admin.site.register(ManagerProfileInfo)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "party_name",
        "party_contact",
        "city",
        "state",
        "country",
        "venue_charge",
        "public_strength",
    )
    list_filter = ("city", "state", "country")
    search_fields = ("name", "party_name", "party_contact", "city", "state", "country")
    fieldsets = (
        ("Venue Details", {
            "fields": ("name", "manager", "party_name", "party_contact", "venue_charge", "public_strength")
        }),
        ("Location Details", {
            "fields": ("address", "city", "pincode", "state", "country")
        }),
    )


@admin.register(RequiredThing)
class RequiredThingAdmin(admin.ModelAdmin):
    list_display = ("name", "price_per_qty", "manager")
    list_filter = ("manager",)
    search_fields = ("name", "manager__name")
    fields = ("name", "price_per_qty", "manager")