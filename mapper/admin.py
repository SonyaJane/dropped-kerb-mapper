from django.contrib import admin
from .models import Report
from django_summernote.admin import SummernoteModelAdmin
from .filters import ReasonsFilter
from .admin_forms import ReportAdminForm  # custom admin form

# Use a decorator to register a class, compared to just registering the standard model
@admin.register(Report)
class ReportAdmin(SummernoteModelAdmin):
    form = ReportAdminForm  # Link the custom form to the admin
    # Fields to be displayed in the admin dashboard
    list_display = ('id', 'classification', 'get_reasons_display', 'photo', 'user', 'created_at')
    # Which fields to search using the search bar
    search_fields = ['reasons', 'comments']
    # Filter options to be displayed on the right side of the dashboard
    list_filter = ('classification', ReasonsFilter, 'user', 'created_at')


