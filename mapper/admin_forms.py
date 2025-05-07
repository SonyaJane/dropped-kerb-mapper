"""
Admin forms for the mapper application.

This module provides ModelForms used in the Django admin:
  • ReportAdminForm: Extends ReportForm to leverage image conversion
    (to webp) and compression when uploading photos via the admin interface.
"""
from .models import Report
from .forms import ReportForm  

class ReportAdminForm(ReportForm):
    """
    ModelForm for the Report model in the Django admin.

    Inherits all logic from ReportForm to ensure:
      - Uploaded images are converted to webp format.
      - Images are compressed to save storage space.
    Includes every field on the Report model for full edit capability.
    """
    class Meta(ReportForm.Meta):
        model = Report
        fields = '__all__'