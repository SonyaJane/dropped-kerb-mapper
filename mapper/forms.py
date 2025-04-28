# When building your form (or in the admin), filter the queryset for reasons so that only options matching the chosen condition are displayed.
# When creating your form or view, you can further customize the reasons field so that the checkboxes dynamically change based on the user's condition choice. For example, in a custom ModelForm, you might override the __init__ method to filter the reasons queryset based on an initial value for the condition field.
#This design keeps the reasons for condition as a field on the DroppedKerbReport, while still allowing you to have a distinct set of reasons available for each traffic light option.

from .models import Report
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Field, Div
from django import forms
# for image size reduction
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model

class ReportForm(forms.ModelForm):
    delete_photo = forms.BooleanField(
        required=False,
        label="Delete current photo",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    class Meta:
        model = Report
        fields = ('latitude', 'longitude', 'condition', 'reasons', 'comments', 'photo')
        widgets = {
            'latitude': forms.TextInput(attrs={'id': 'latitude'}),
            'longitude': forms.TextInput(attrs={'id': 'longitude'}),
            'condition': forms.Select(attrs={'id': 'condition'}), 
            'reasons': forms.SelectMultiple(attrs={'id': 'reasons'}),
            'photo': forms.FileInput(attrs={'accept': 'image/*'}), 
        }

    def __init__(self, *args, **kwargs):
        # Pop the current user from kwargs and assign to an instance variable
        self.current_user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Make latitude and longitude uneditable
        self.fields['latitude'].widget.attrs['readonly'] = True
        self.fields['longitude'].widget.attrs['readonly'] = True
        self.fields['latitude'].required = False
        self.fields['longitude'].required = False
        self.fields['latitude'].label = ""
        self.fields['longitude'].label = ""
        
        self.fields['condition'].empty_label = None  # Remove the default '-------' option
        self.fields['condition'].choices = [choice for choice in self.fields['condition'].choices if choice[0]]  # Remove empty choice        
        self.fields['condition'].initial = 'green'
        self.fields['condition'].label = ""
        self.fields['reasons'].label = ""
        self.fields['comments'].label = ""
        self.fields['photo'].label = ""

        # Set the layout for the form using crispy-forms
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'

        self.helper.layout = Layout(
            Div(
                HTML('<label for="id_latitude" class="col-4 col-form-label">Latitude</label>'),
                Field('latitude', wrapper_class='col-8'),
                css_class='row mt-2 mt-sm-0'
            ),
            Div(
                HTML('<label for="id_longitude" class="col-4 col-form-label">Longitude</label>'),
                Field('longitude', wrapper_class='col-8'),
                css_class='row mt-2 mt-sm-0'
            ),
            Div(
                HTML('<label for="id_condition" class="col-4 col-form-label">Condition</label>'),
                Field('condition', wrapper_class='col-8'),
                css_class='row mt-2 mt-sm-0'
            ),
            # Custom layout for the reasons field, required to force col-md-4 and col-md-8 classes on choices.js field
            HTML("""
                <div class="row">
                    <div class="col-12 col-sm-4" id="reasons-label">
                        <label for="id_reasons" class="col-form-label">Reasons</label>
                    </div>
                    <div class="col-12 col-sm-8">
            """),
            Field('reasons'), 
            HTML("""
                    </div>
                </div>
            """),       
            # Comments field with custom label class
            Div(
                HTML('<label for="id_comments" class="col-12 col-sm-4 col-form-label">Comments</label>'),
                Field('comments', wrapper_class='col-12 col-sm-8'),
                css_class='row'
            ),
            # Photo field with custom label class
            Div(
                HTML('<label for="id_photo" class="col-12 col-sm-4 col-form-label">Photo</label>'),
                Field('photo', wrapper_class='col-12 col-sm-8'),
                css_class='row'
            ),
            # Display the current photo
            HTML("""
                {% if report.photo %}
                    <div class="form-group">
                        <label class = 'col-12 col-md-4'>Current Photo</label>
                        <img src="{{ report.photo.url }}" alt="Current Photo" style="max-width: 200px; height: auto;" class='col-12 col-md-8'>
                    </div>
                    <div class="form-group">
                        {{ form.delete_photo.label_tag }}
                        {{ form.delete_photo }}
                    </div>
                {% endif %}
            """),
            Submit('submit', 'Submit', css_class='btn btn-green', css_id='report-submit-btn'),
            # Cancel button
            HTML("""
                {% if is_map_reports %}
                    <a href="javascript:void(0);" class="btn close-btn btn-mango" id="report-cancel-btn">Cancel</a>
                {% else %} 
                    {% if report.id %}
                        <a href="{% url 'report-detail' report.id %}" class="btn btn-mango">Cancel</a>
                    {% else %}
                        <a href="{% url 'reports-list' %}" class="btn btn-mango">Cancel</a>
                    {% endif %}   
                {% endif %}          
                """),   
        )
                
    def clean_photo(self):
        """
        Custom clean method converts the image format to webp, and compresses it if the result exceeds a certain size.
        """
        photo = self.cleaned_data.get('photo')
        delete_photo = self.data.get('delete_photo')  # Check if the delete_photo checkbox is checked
        print(f"delete_photo: {delete_photo}")
        
        # Skip processing if delete_photo is checked
        if delete_photo == 'on':
            print("Photo deletion requested, skipping photo processing.")
            return None
    
        # Skip processing if the photo is a CloudinaryResource (already uploaded)
        if photo and not hasattr(photo, 'read'):
            print("Photo is a CloudinaryResource, skipping processing.")
            return photo
    
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
    
    def clean(self):
        cleaned_data = super().clean()
        condition = cleaned_data.get('condition')
        reasons = cleaned_data.get('reasons')
        # If condition is red or orange, ensure that at least one reason is selected.
        if condition in ['red', 'orange'] and (not reasons or len(reasons) == 0):
            self.add_error('reasons', "At least one reason must be selected when condition is red or orange.")
            
        # Check permissions: allow edit only if the current user is the original owner or a superuser.
        if self.instance.pk and self.current_user:
            if self.instance.user != self.current_user and not self.current_user.is_superuser:
                raise forms.ValidationError("You do not have permission to edit this report.")

        return cleaned_data
    

# SIGNUP FORM
class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label="First Name", required=True)
    last_name = forms.CharField(max_length=30, label="Last Name", required=True) 
    
    uses_mobility_device = forms.TypedChoiceField(
        label="Do you use a wheeled mobility device?",
        required=False,
        choices=((False, 'No'),(True, 'Yes')),
        coerce=lambda x: x == 'True',  # converts the posted value to boolean
        widget=forms.Select,
    )
    
    # Define choices for mobility devices.
    MOBILITY_DEVICE_CHOICES = (
        ('manual_wheelchair', 'Manual Wheelchair'),
        ('powered_wheelchair', 'Powered Wheelchair'),
        ('mobility_scooter', 'Mobility Scooter'),
        ('tricycle', 'Tricycle'),
        ('adapted_bicycle', 'Adapted Bicycle'),
        ('bicycle', 'Bicycle'),
        ('other', 'Other'),
    )
    
    mobility_device_type = forms.ChoiceField(
        label="Please select your mobility device:",
        choices=MOBILITY_DEVICE_CHOICES,
        required=False,
    )
      
    is_carer = forms.TypedChoiceField(
        label="Do you care for someone who uses a wheeled mobility device?",
        required=False,
        choices=((False, 'No'),(True, 'Yes')),
        coerce=lambda x: x == 'True',  # converts the posted value to boolean
        widget=forms.Select,
    )
    
    mobility_device_type_caree = forms.ChoiceField(
        label="Please select the mobility device used by the person you care for:",
        choices=MOBILITY_DEVICE_CHOICES,
        required=False,
    )
    
    # Existing fields for mobility devices, etc.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Create FormHelper for styling
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        # Apply custom classes to labels and fields
        self.helper.label_class = 'col-12 col-sm-4'
        self.helper.field_class = 'col-12 col-sm-8'
    
    def clean(self):
        cleaned_data = super().clean()
        uses = cleaned_data.get('uses_mobility_device')
        device = cleaned_data.get('mobility_device_type')
        
        if uses and not device:
            self.add_error('mobility_device_type', "Please select your mobility device type.")
        return cleaned_data

    def save(self, request):
        User = get_user_model()  # Get the user model
        user = super(CustomSignupForm, self).save(request)
        first = self.cleaned_data.get('first_name').strip().lower()
        last = self.cleaned_data.get('last_name').strip().lower()
        base_username = f"{first}_{last}"
        username = base_username
        
        # Ensure the username is unique
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1
        user.first_name = first.capitalize()
        user.last_name = last.capitalize()
        user.username = username
        
        # Set the mobility device fields
        user.uses_mobility_device = self.cleaned_data.get('uses_mobility_device')
        user.mobility_device_type = self.cleaned_data.get('mobility_device_type')
        user.save()
        
        return user
    
    
class ContactForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        label="First Name",
        required=True
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        label="Last Name",
        required=True
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        label="Email Address",
        required=True
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}),
        label="Your Message"
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from the kwargs
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            # Pre-fill fields with user data and make them read-only
            self.fields['first_name'].initial = user.first_name
            self.fields['first_name'].widget.attrs['readonly'] = True
            self.fields['last_name'].initial = user.last_name
            self.fields['last_name'].widget.attrs['readonly'] = True
            self.fields['email'].initial = user.email
            self.fields['email'].widget.attrs['readonly'] = True