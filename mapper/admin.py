from django.contrib import admin
from .models import Report, Photo
from django_summernote.admin import SummernoteModelAdmin
from .filters import ReasonsFilter

# Register your models here.

# Use a decorator to register a class, compared to just registering the standard model
@admin.register(Report)
class ReportAdmin(SummernoteModelAdmin):
    # Fields to be displayed in the admin dashboard
    list_display = ('id', 'classification', 'get_reasons_display', 'user', 'created_at')
    # Which fields to search using the search bar
    search_fields = ['reasons', 'comments']
    # Filter options to be displayed on the right side of the dashboard
    list_filter = ('classification', ReasonsFilter, 'user', 'created_at')
    # Create WYSIWYG editor for the comments field
    summernote_fields = ('comments',)
    
admin.site.register(Photo)

