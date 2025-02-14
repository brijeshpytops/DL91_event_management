from django.contrib import admin
from apps.wines.models import Wine


@admin.register(Wine)
class WineAdmin(admin.ModelAdmin):
    list_display = ('manager_name', 'wine_name', 'wine_price', 'wine_type', 'alcohol_content', 'wine_qty_ml')
    search_fields = ('wine_name', 'wine_type', 'alcohol_content')
    list_filter = ('wine_type',)
    ordering = ('wine_name',)
    list_editable = ('wine_price', 'wine_qty_ml')
    list_per_page = 20
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('manager', 'wine_name', 'wine_type', 'wine_price')
        }),
        ('Details', {
            'fields': ('alcohol_content', 'wine_qty_ml')
        }),
    )

    def manager_name(self, obj):
        """Display the manager's name in the admin panel."""
        return f"{obj.manager.first_name} {obj.manager.last_name}"  # Adjust based on your Manager model
    manager_name.admin_order_field = 'manager'  # Allow sorting
    manager_name.short_description = 'Manager Name'

