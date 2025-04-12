from django.contrib import admin
from .models import Report
from django_summernote.admin import SummernoteModelAdmin
from .filters import ReasonsFilter
from .admin_forms import ReportAdminForm  # custom admin form
from .models import County
from django.contrib.gis import admin as geo_admin

# Use a decorator to register a class, compared to just registering the standard model
@admin.register(Report)
class ReportAdmin(SummernoteModelAdmin):
    form = ReportAdminForm  # Link the custom form to the admin
    # Fields to be displayed in the admin dashboard
    list_display = ('id', 'county', 'classification', 'get_reasons_display', 'photo', 'user', 'created_at')
    # Which fields to search using the search bar
    search_fields = ['reasons', 'comments']
    # Filter options to be displayed on the right side of the dashboard
    list_filter = ('classification', ReasonsFilter, 'user', 'created_at')

# register the County model with the admin site
admin.site.register(County, geo_admin.ModelAdmin)
# @admin.register(County)
# class CountyAdmin(OSMGeoAdmin):
#     list_display = ('name',)
#     search_fields = ['name']
#     list_filter = ['name']
#     # Use the OSMGeoAdmin to display the map in the admin interface    
