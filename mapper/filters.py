from django.contrib.admin import SimpleListFilter
from .models import Report


class ReasonsFilter(SimpleListFilter):
    """
    Custom admin filter for Report.reasons.

    The MultiSelectField stores its data as a comma-separated
    string in the database. Django's built-in filtering in the
    admin interface isnt designed to parse that string.
    This filter allows the admin to filter reports based on
    the condition choice reasons.

    Presents the Report.ALLOWED_REASONS choices in the sidebar
    and filters the queryset based on whether the selected reason
    appears in the  comma-separated `reasons` field (using a
    case-insensitive `icontains` lookup).
    """
    title = 'Reasons'
    parameter_name = 'reasons'

    def lookups(self, request, model_admin):
        """
        Return the list of filter options for reasons.

        Args:
            request (HttpRequest): The current HTTP request.
            model_admin (ModelAdmin): The admin site's ModelAdmin instance.

        Returns:
            list[tuple]: Tuples of (value, label) from Report.ALLOWED_REASONS.
        """
        # Returns the list of ALLOWED_REASONS defined in the
        # model as a list of tuples.
        return Report.ALLOWED_REASONS

    def queryset(self, request, queryset):
        """
        Filter the Report queryset by the selected reason.

        Args:
            request (HttpRequest): The current HTTP request.
            queryset (QuerySet): Base Report queryset to filter.

        Returns:
            QuerySet: Filtered reports where `reasons` contains
            the selected value, or the original queryset if no
            filter is applied.
        """
        # If no value is selected, return the entire queryset.
        if self.value():
            # Filter reports where the reasons field contains
            # the selected reason.
            # Note: __icontains is used here to perform a
            # case-insensitive search.
            return queryset.filter(reasons__icontains=self.value())
        return queryset
