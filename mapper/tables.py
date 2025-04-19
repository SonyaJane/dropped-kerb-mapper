import django_tables2 as tables
from .models import Report

class ReportTable(tables.Table):
    # Show a link to the photo if it exists, otherwise show a dash
    photo = tables.TemplateColumn(
        verbose_name="Photo",
        template_code='''            
            {% if record.photo %}
                <a href="{{ record.photo.url }}" target="_blank" rel="noopener noreferrer">Photo</a>
            {% else %}
                —
            {% endif %}
        ''',
        orderable=False
    )
    place_name = tables.TemplateColumn(
        template_code='''{% load comma_wrap %}{{ record.place_name|comma_wrap }}''',
        attrs={"td": {"style": "white-space: nowrap;"}}
    )
    county = tables.TemplateColumn(
        template_code='''{% load comma_wrap %}{{ record.county|comma_wrap }}''',
        attrs={"td": {"style": "white-space: nowrap;"}}
    )
    local_authority = tables.TemplateColumn(
        verbose_name="LA",
        template_code='''{% load comma_wrap %}{{ record.local_authority|comma_wrap }}''',
        attrs={"td": {"style": "white-space: nowrap;"}}
    )
    reasons = tables.TemplateColumn(
        template_code='''{% load comma_wrap %}{{ record.reasons|comma_wrap }}''',
        attrs={"td": {"style": "white-space: nowrap;"}}
    )
    comments = tables.Column(
        attrs={"td": {"class": "la-width"}, "th": {"class": "la-width"}}  # increase width for the column
    )
    created_at = tables.Column(
        verbose_name="Created",
        attrs={"td": {"style": "white-space: nowrap;"}}
    )
    updated_at = tables.Column(
        verbose_name="Updated",
        attrs={"td": {"style": "white-space: nowrap;"}}
    )
    
    def render_created_at(self, value):
        # Format the date as "day, month (name), year" e.g. "1 September 2025"
        # Note: on Windows use "%#d" instead of "%-d" if leading zeros become an issue.
        return value.strftime("%#d %B %Y %H:%M")
        # return value.strftime("%-d %B %Y %H:%M") #  non-windows
    
    def render_updated_at(self, value):
        # Format the date as "day, month (name), year" e.g. "1 September 2025"
        # Note: on Windows use "%#d" instead of "%-d" if leading zeros become an issue.
        return value.strftime("%#d %B %Y %H:%M")
        # return value.strftime("%-d %B %Y %H:%M") #  non-windows
        
    class Meta:
        model = Report
        template_name="django_tables2/bootstrap5-responsive.html"
        fields = (
            'id',
            'user',
            'user_report_number',
            'latitude',
            'longitude',
            'place_name',
            'county',
            'local_authority',
            'condition',
            'reasons',
            'comments',
            'photo',
            'created_at',
            'updated_at')