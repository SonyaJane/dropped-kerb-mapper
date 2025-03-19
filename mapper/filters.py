from django.contrib.admin import SimpleListFilter
from .models import Report

# Custom admin filter for the Report model
# The MultiSelectField stores its data as a comma‑separated string in the database.
# Django’s built‑in filtering in the admin isnt designed to parse that string.
# This function is a custom admin filter using Django’s SimpleListFilter to filter 
# the queryset based on whether a particular allowed reason is present in the field.

class ReasonsFilter(SimpleListFilter):
    title = 'Reasons'
    parameter_name = 'reasons'

    def lookups(self, request, model_admin):
        # Returns the list of ALLOWED_REASONS defined in the model as a list of tuples.
        return Report.ALLOWED_REASONS

    def queryset(self, request, queryset):
        # If no value is selected, return the entire queryset.
        if self.value():
            # Filter reports where the reasons field contains the selected reason.
            # Note: __icontains is used here to perform a case-insensitive search.
            return queryset.filter(reasons__icontains=self.value())
        return queryset