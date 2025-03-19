from django.contrib import admin
from .models import Report, Photo
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

# Use a decorator to register a class, compared to just registering the standard model
@admin.register(Report)
class ReportAdmin(SummernoteModelAdmin):
    list_display = ('id', 'classification', 'reasons', 'user')
    search_fields = ['classification', 'reasons', 'user']
    list_filter = ('classification', 'reasons', 'user')
    #prepopulated_fields = {'slug': ('classification',)}
    summernote_fields = ('comments',)
    
admin.site.register(Photo)

