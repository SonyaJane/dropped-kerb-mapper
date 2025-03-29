from .models import Report
from .forms import ReportForm  

# Reuse the existing form so that the image is converted to webp format and compressed
# when uploaded in the admin dashboard as well.
# This is important to keep the image size down and save space in the database.

class ReportAdminForm(ReportForm):
    class Meta(ReportForm.Meta):
        model = Report
        fields = '__all__'