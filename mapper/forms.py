# When building your form (or in the admin), filter the queryset for reasons so that only options matching the chosen classification are displayed.
# When creating your form or view, you can further customize the reasons field so that the checkboxes dynamically change based on the user's classification choice. For example, in a custom ModelForm, you might override the __init__ method to filter the reasons queryset based on an initial value for the classification field.
#This design keeps the reasons for classification as a field on the DroppedKerbReport, while still allowing you to have a distinct set of reasons available for each traffic light option.

from .models import Report
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Field, HTML
from django import forms
# for image size reduction
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['latitude', 'longitude', 'classification', 'reasons', 'comments', 'photo']
        widgets = {
            'latitude': forms.TextInput(attrs={'id': 'latitude'}),
            'longitude': forms.TextInput(attrs={'id': 'longitude'}),
            'classification': forms.Select(attrs={'id': 'classification'}), 
            'reasons': forms.SelectMultiple(attrs={'id': 'reasons', 'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'accept': 'image/*'}), 
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['classification'].empty_label = None  # Remove the default '-------' option
        self.fields['classification'].choices = [choice for choice in self.fields['classification'].choices if choice[0]]  # Remove empty choice        
        self.fields['classification'].initial = 'green'   # Set the default value to "green"
        self.fields['reasons'].label = ''                 # Remove the header for the reasons field

        # Set the layout for the form using crispy-forms
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-4'   # Labels in 3/12 of the row
        self.helper.field_class = 'col-8'   # Fields in 9/12 of the row
        
        self.helper.layout = Layout(
            'latitude',
            'longitude',
            'classification',
            HTML('<p class="reasons-help-text">Select one or more reasons:</p>'),  # Add help text above the reasons field
            'reasons',         
            'comments',
            'photo',
        )
        
    def clean_photo(self):
        """
        Custom clean method converts the image format to webp, and compresses it if the result exceeds a certain size.
        """
        print("Starting cleaning photo")
        photo = self.cleaned_data.get('photo')
        if photo:
            # convert image to webp format:
            try:
                # Open the image using PIL
                image = Image.open(photo)
                print('opened photo')
                # Convert to RGB as webp does not support RGBA
                image = image.convert("RGB") 
                print('converted photo to RGB')
                # Create a BytesIO object to save the image
                output = BytesIO() 
                image.save(output, format='WEBP')
                output.seek(0) # Reset the pointer to the start of the BytesIO object
                
                # check if the image size exceeds the limit
                max_size = 5 * 1024 * 1024  # 5MB in bytes
                if output.getbuffer().nbytes > max_size:
                    # If it does, reduce the quality iteratively starting from 85
                    quality = 85
                    while output.getbuffer().nbytes > max_size and quality > 10:
                        quality -= 5  # Lower the quality by 5 units
                        output = BytesIO()  # Reset the in-memory buffer
                        image.save(output, format="WEBP", quality=quality)
                        output.seek(0)
                
                # Update the filename to have a .webp extension
                new_filename = photo.name.rsplit('.', 1)[0] + '.webp'
                print("Photo converted to webp format")
                # Create a new InMemoryUploadedFile with the converted WebP image
                photo = InMemoryUploadedFile(
                    output,
                    'ImageField',
                    new_filename,
                    'image/webp',
                    output.getbuffer().nbytes,
                    None
                )
            except Exception as e:
                raise forms.ValidationError(f"Error processing image: {str(e)}")
        return photo