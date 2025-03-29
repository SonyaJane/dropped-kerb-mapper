# When building your form (or in the admin), filter the queryset for reasons so that only options matching the chosen classification are displayed.
# When creating your form or view, you can further customize the reasons field so that the checkboxes dynamically change based on the user's classification choice. For example, in a custom ModelForm, you might override the __init__ method to filter the reasons queryset based on an initial value for the classification field.
#This design keeps the reasons for classification as a field on the DroppedKerbReport, while still allowing you to have a distinct set of reasons available for each traffic light option.

from .models import Report
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
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
            'classification': forms.RadioSelect,      
            'reasons': forms.CheckboxSelectMultiple(attrs={'id': 'reasons'}),
            'photo': forms.ImageField,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['classification'].empty_label = None  # Remove the default '-------' option
        self.fields['classification'].choices = [choice for choice in self.fields['classification'].choices if choice[0]]  # Remove empty choice        
        self.fields['classification'].initial = 'green'  # Set the default value to "green"        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit Report'))
        
    from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

def clean_photo(self):
    """
    Custom clean method to compress the uploaded image if it exceeds a certain size.
    """
    photo = self.cleaned_data.get('photo')
    if photo:
        max_size = 5 * 1024 * 1024  # 5MB in bytes
        # Only attempt compression if the original file is over the limit.
        if photo.size > max_size:
            try:
                # Open the uploaded image with Pillow
                img = Image.open(photo)
                # Convert the image to RGB if necessary (JPEG does not support alpha channels)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                
                # Set initial quality (start high and reduce as needed)
                quality = 85
                # Create a buffer for the in-memory image
                output = BytesIO()
                
                # Save image to the buffer with the initial quality setting
                img.save(output, format="JPEG", quality=quality)
                
                # While the size is still above max_size and quality is above a threshold, reduce quality.
                while output.getbuffer().nbytes > max_size and quality > 10:
                    quality -= 5  # Decrease quality
                    output = BytesIO()  # Reset the buffer
                    img.save(output, format="JPEG", quality=quality)
                
                # Reset the file pointer of the buffer. Ensures that when we later read from the buffer (or pass it to another function), the read operation starts at the very beginning of the data. 
                output.seek(0)
                
                # Replace the original photo with the compressed version.
                photo = InMemoryUploadedFile(
                    output,
                    'ImageField',
                    photo.name,
                    'image/jpeg',
                    output.getbuffer().nbytes,
                    None
                )
            except Exception as e:
                raise forms.ValidationError("Error processing image: " + str(e))
    return photo
