"""
Admin configuration for the mapper application.

Registers and configures the Django admin interfaces for:
  • Report (with custom filtering/form),
  • County and LocalAuthority (GeoDjango ModelAdmin),
  • CustomUser (extends UserAdmin with extra profile fields).
"""
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Report, County, LocalAuthority
from .filters import ReasonsFilter
from .admin_forms import ReportAdminForm  # custom admin form
from django.contrib.gis import admin as geo_admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(Report)
class ReportAdmin(ImportExportModelAdmin):
    """
    Admin interface for the Report model.

    - Uses ReportAdminForm to customize form layout and validation.
    - Displays key fields in list_display for quick overview.
    - Enables search on reasons and comments.
    - Adds sidebar filters for condition, reasons, user, and created_at.
    """
    form = ReportAdminForm  # Link the custom form to the admin
    # Fields to be displayed in the admin dashboard
    list_display = ('id', 'place_name', 'county', 'condition', 
                    'get_reasons_display', 'comments', 'photo', 
                    'user', 'created_at')
    # Which fields to search using the search bar
    search_fields = ['reasons', 'comments']
    # Filter options to be displayed on the right side of the dashboard
    list_filter = ('condition', ReasonsFilter, 'user', 'created_at')


# register the area models with the admin site
admin.site.register(County, geo_admin.ModelAdmin)


admin.site.register(LocalAuthority, geo_admin.ModelAdmin)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin interface for the CustomUser model.

    Extends Django's built-in UserAdmin to include:
      - uses_mobility_device
      - mobility_device_type
      - is_carer
    in both the user detail and user creation forms.
    """
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('uses_mobility_device',
                           'mobility_device_type',
                           'is_carer')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('uses_mobility_device',
                           'mobility_device_type',
                           'is_carer')}),
    )
