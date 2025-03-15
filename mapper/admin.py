from django.contrib import admin
from .models import ClassificationReason, Report, Photo
# Register your models here.

admin.site.register(ClassificationReason)
admin.site.register(Report)
admin.site.register(Photo)
