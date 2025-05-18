"""
Defines the ReportTable for the mapper app using django-tables2.

This module provides:
  - ReportTable: a Bootstrap-responsive table for Report instances.
  - Custom columns and template columns for view/edit actions.
  - Modal-enabled photo preview without exposing URLs to regular users.
  - Formatted place_name, county, local_authority, and reasons with comma
    wrapping.
  - Human-readable created_at and updated_at renderers using
    Windows-compatible formats.
"""
import django_tables2 as tables
from .models import Report

class ReportTable(tables.Table):
    """
     Table representation for Report instances.

     Renders a responsive, Bootstrap-styled table with the following features:
       - view: link icon to view report details
       - edit: link icon to edit the report
       - photo: shows a camera icon linking to the image or opens a modal
        (based on user role)
       - formatted place_name, county, local_authority, and reasons columns
       - human-readable created_at and updated_at timestamps
     """
    # Show a link to the photo if it exists, otherwise show a dash
    photo = tables.TemplateColumn(
        verbose_name="Photo",
        # Superusers see the external link (URL revealed)
        # Non‑superusers opens a modal popup showing the image, 
        # without exposing the URL in an <a> tag.
        template_code='''
            {% if record.photo %}
                <!-- Button to trigger Bootstrap modal -->
                <button
                    type="button"
                    class="btn btn-link p-0"
                    data-bs-toggle="modal"
                    data-bs-target="#photoModal{{ record.id }}"
                    aria-label="View photo"
                >
                <i class="bi bi-camera-fill"></i>
                </button>
                <!-- Modal -->
                <div 
                    class="modal fade"
                    id="photoModal{{ record.id }}"
                    tabindex="-1"
                    aria-labelledby="photoModalLabel{{ record.id }}"
                    aria-hidden="true"
                >
                    <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content bg-transparent border-0">
                        <img
                        src="{{ record.photo.url }}"
                        class="img-fluid"
                        alt="Report {{ record.id }} photo"
                        >
                    </div>
                </div>
            <!--No photo available-->
            {% else %}
                —
            {% endif %}
        ''',
        orderable=False,
        attrs={"td": {"class": "text-center align-middle"}}
    )
    user_report_number = tables.Column(
        verbose_name="Report",
    )
    place_name = tables.TemplateColumn(
        template_code='''{% load comma_wrap %}\
            {{ record.place_name|comma_wrap }}''',
        attrs={"td": {"style": "white-space: nowrap;"}}
    )
    county = tables.TemplateColumn(
        template_code='''{% load comma_wrap %}\
            {{ record.county|comma_wrap }}''',
        attrs={"td": {"style": "white-space: nowrap;", "class": "align-middle"},}
    )
    local_authority = tables.TemplateColumn(
        verbose_name="LA",
        template_code='''{% load comma_wrap %}\
            {{ record.local_authority|comma_wrap }}''',
        attrs={"td": {"style": "white-space: nowrap;"}}
    )
    reasons = tables.TemplateColumn(
        template_code='''{% load comma_wrap %}\
            {{ record.reasons|comma_wrap }}''',
        attrs={"td": {"style": "white-space: nowrap;", "class": "text-center align-middle"},}
    )
    created_at = tables.Column(
        verbose_name="Created",
        attrs={"td": {"style": "white-space: nowrap;", "class": "text-center align-middle"},}
    )
    updated_at = tables.Column(
        verbose_name="Updated",
        attrs={"td": {"style": "white-space: nowrap;", "class": "text-center align-middle"},}
    )
    # New column - link to view the report details (eye icon)
    view = tables.TemplateColumn(
        verbose_name="View",
        template_code='''<a href="{% url 'report-detail' record.id %}" aria-label="View report details">
                         <i class="bi bi-eye-fill"></i></a>''',
        orderable=False,
        attrs={"td": {"class": "text-center align-middle"}}

    )
    edit = tables.TemplateColumn(
        verbose_name="Edit",
        template_code='''<a href="{% url 'edit-report' record.id %}" aria-label="Edit report details">
                         <i class="bi bi-pencil-fill"></i></a>''',
        orderable=False,
        attrs={"td": {"class": "text-center align-middle"}}

    )
    # delete
    delete = tables.TemplateColumn(
        verbose_name="Delete",
        template_code='''
            <button type="button"
                    class="btn btn-link p-0 delete-report-btn"
                    data-bs-toggle="modal"
                    data-bs-target="#delete-modal"
                    data-report-id="{{ record.id }}"
                    aria-label="Delete report">
                <i class="bi bi-trash-fill"></i>
            </button>
        ''',
        orderable=False,
        attrs={"td": {"class": "text-center align-middle"}}    
    )
    def render_created_at(self, value):
        """
        Format the created_at datetime for display.

        Converts the datetime to a string like "1 September 2025 14:30",
        using a Windows-compatible day format ("%#d") to avoid leading zeros.
        """
        return value.strftime("%#d %B %Y %H:%M")    # Windows
        # return value.strftime("%-d %B %Y %H:%M")  # non-windows

    def render_updated_at(self, value):
        """
        Format the updated_at datetime for display.

        Converts the datetime to a string like "1 September 2025 14:30",
        using a Windows-compatible day format ("%#d") to avoid leading zeros.
        """
        return value.strftime("%#d %B %Y %H:%M")    # Windows
        # return value.strftime("%-d %B %Y %H:%M")  # non-windows

    class Meta:
        model = Report
        template_name="django_tables2/bootstrap5-responsive.html"
        fields = (
            'id',
            'user_report_number',
            'view',
            'edit',
            'delete',
            'photo',
            'user',
            'latitude',
            'longitude',
            'place_name',
            'county',
            'local_authority',
            'condition',
            'reasons',
            'comments',
            'created_at',
            'updated_at',
            )
        attrs = {
        "td": {"class": "align-middle"},
    }
