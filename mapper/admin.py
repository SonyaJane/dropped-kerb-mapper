from django.contrib import admin
from .models import Report, Photo
# Register your models here.

# class ReportAdmin(admin.ModelAdmin):
#     list_display = ('classification', 'user', 'created_at')
    
#     class Media:
#         js = ('js/report_admin.js',)

#admin.site.register(Report, ReportAdmin)

admin.site.register(Report)
admin.site.register(Photo)

