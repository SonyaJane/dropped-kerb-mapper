# When building your form (or in the admin), filter the queryset for reasons so that only options matching the chosen classification are displayed.
# When creating your form or view, you can further customize the reasons field so that the checkboxes dynamically change based on the user's classification choice. For example, in a custom ModelForm, you might override the __init__ method to filter the reasons queryset based on an initial value for the classification field.
#This design keeps the reasons for classification as a field on the DroppedKerbReport, while still allowing you to have a distinct set of reasons available for each traffic light option.

from .models import Report
from django import forms
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['classification', 'reasons']