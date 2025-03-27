# When building your form (or in the admin), filter the queryset for reasons so that only options matching the chosen classification are displayed.
# When creating your form or view, you can further customize the reasons field so that the checkboxes dynamically change based on the user's classification choice. For example, in a custom ModelForm, you might override the __init__ method to filter the reasons queryset based on an initial value for the classification field.
#This design keeps the reasons for classification as a field on the DroppedKerbReport, while still allowing you to have a distinct set of reasons available for each traffic light option.

from .models import Report, Photo
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

class ReportForm(forms.ModelForm):
    # photos = forms.FileField(
    #     required=False,
    #     widget=forms.FileInput(attrs={'multiple': True}),
    #     label="Upload Photos (up to 3)"
    # )
    class Meta:
        model = Report
        fields = ['latitude', 'longitude', 'classification', 'reasons', 'comments']# , 'photos']
        widgets = {
            'classification': forms.RadioSelect,      
            'reasons': forms.CheckboxSelectMultiple(attrs={'id': 'reasons'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['classification'].empty_label = None  # Remove the default '-------' option
        self.fields['classification'].choices = [choice for choice in self.fields['classification'].choices if choice[0]]  # Remove empty choice        
        self.fields['classification'].initial = 'green'  # Set the default value to "green"        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit Report'))