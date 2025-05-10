"""
Form definitions

- ReportForm:
    A ModelForm for creating and editing dropped-kerb Report instances.
    Handles map-populated latitude/longitude, condition, reasons, comments,
    photo uploads, optional photo deletion, and enforces field validation
    and image processing (conversion to WebP, size compression).

- CustomSignupForm:
    Extends allauth's SignupForm to collect first/last name, auto-generate
    a unique username, ask if the user is a wheeled mobility device user or if they
    care for someone who does, and capture mobility device usage details.

- ContactForm:
    A simple contact-us Form collecting first name, last name, email, and
    message. Pre-populates and locks fields for authenticated users.

- CustomLoginForm:
    Extends allauth's LoginForm to remove the 'Remember Me' option and
    apply Crispy Forms styling without its default <form> wrapper.
"""
from io import BytesIO
import logging
from django import forms
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from allauth.account.forms import SignupForm, LoginForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Field, Div
from cloudinary import uploader
from cloudinary.exceptions import Error as CloudinaryError
from .models import Report, CustomUser

logger = logging.getLogger(__name__) # Set up logging for this module

class ReportForm(forms.ModelForm):
    """
    A ModelForm for creating and editing dropped-kerb Report instances.
    - Fields:
        • latitude (readonly text, auto-populated by map)
        • longitude (readonly text, auto-populated by map)
        • condition (select: none, green, orange, red, white)
        • reasons (multi-select, shown only for red/orange)
        • comments (text area)
        • photo (file upload)
        • delete_photo (radio: remove existing image)
    - Layout via Crispy Forms for responsive styling.
    - Overrides clean_photo() to convert and compress uploads to WebP.
    - Validates reasons vs. condition and edit permissions in clean().
    - Deletes existing photo if requested in handle_delete_photo().
    - Custom save() to apply deletion, assign new photo, and persist.
    """
    delete_photo = forms.TypedChoiceField(
        label="Delete current photo?",
        required=False,
        choices=(
            ('False', 'No'),
            ('True', 'Yes'),
        ),
        coerce=lambda val: val == 'True',
        initial='False',
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-inline',
        }),
    )
    class Meta:
        """
        Meta options for ReportForm.

        - model: The Report model to create/edit.
        - fields: Tuple of model fields to include in the form
          ('latitude', 'longitude', 'condition', 'reasons', 'comments', 'photo').
        - widgets: Dict mapping each field to a custom widget with specific
          attributes (e.g., #id, accept image rule) for integration with the map
          interface and frontend scripts.
        """
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
        """
        Initialise the ReportForm with map integration and user context.

        - Pops 'user' from kwargs and stores it as self.current_user for
          permission checks in clean() and save().
        - Calls the parent __init__ to bind data and files.
        - Marks latitude/longitude fields as readonly, and hides labels
          to allow map-driven population.
        - Sets up default choices and initial values for 'condition'.
        - Clears labels on all fields for custom layout.
        - Instantiates a Crispy Forms FormHelper and defines the form layout
          with responsive rows, labels, and submit/cancel buttons.

        Args:
            *args: Positional arguments forwarded to the ModelForm.
            **kwargs: Keyword arguments; expects optional 'user' key.
        """
        # Pop the current user from kwargs and assign to an instance variable
        self.current_user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Make latitude and longitude uneditable
        self.fields['latitude'].widget.attrs['readonly'] = True
        self.fields['longitude'].widget.attrs['readonly'] = True
        self.fields['latitude'].label = ""
        self.fields['longitude'].label = ""
        self.fields['condition'].empty_label = None  # Remove the default '-------' option
        # Remove empty choice from condition field
        self.fields['condition'].choices = \
            [choice for choice in self.fields['condition'].choices if choice[0]]
        self.fields['condition'].initial = 'none'
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
            # Custom layout for the reasons field, required to force col-md-4 and col-md-8 
            # classes on choices.js field and make it intially hidden
            HTML("""
                <div class="row hidden" id="reasons-container">
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
                HTML('<label for="id_comments" class="col-12 col-sm-4 col-form-label">\
                        Comments\
                      </label>'),
                Field('comments', wrapper_class='col-12 col-sm-8'),
                css_class='row'
            ),
            # Display the current photo
            HTML("""
                {% if report.photo %}
                    <div class="form-group">
                        <label class = 'col-12 col-md-4 fw-normal mb-2'>Current Photo</label>
                        <img src="{{ report.photo.url }}" alt="Current Photo" class='col-12 col-md-8 current-photo'>
                    </div>
                    <div class="row my-2 align-items-center">
                        <label for="id_delete_photo"
                            class="fw-normal col-12 col-sm-5 col-form-label">
                        Delete Current Photo?
                        </label>
                        <div class="col-12 col-sm-7">
                        {{ form.delete_photo }}
                        </div>
                    </div>
                    <p>Uploading a new photo replaces the current photo.</p>
                {% endif %}
            """),
            # Photo field with custom label class
            Div(
                HTML('<label for="id_photo"\
                            class="col-12 col-sm-4 col-form-label">New Photo</label>'),
                Field('photo', wrapper_class='col-12 col-sm-8'),
                css_class='row'
            ),
            Submit('submit', 'Submit', css_class='btn btn-green report-submit-btn'),
            # Cancel button
            HTML("""
                {% if is_map_reports %}
                    <a href="javascript:void(0);" class="btn btn-mango report-cancel-btn">Cancel</a>
                {% else %} 
                    {% if report.id %}
                        <a href="{% url 'report-detail' report.id %}" class="btn btn-mango report-cancel-btn">Cancel</a>
                    {% else %}
                        <a href="{% url 'reports-list' %}" class="btn btn-mango report-cancel-btn">Cancel</a>
                    {% endif %}   
                {% endif %}          
                """),
        )

    def clean_photo(self):
        """
        Validate and process the uploaded photo for WebP conversion and compression.

        - If `photo` already exists and therefore is a CloudinaryResource \
            (no `read` method), returns it unchanged.
        - Converts newly uploaded images to WebP format.
        - Ensures the file size does not exceed 5 MB by iteratively reducing quality.
        - Wraps the final bytes in an InMemoryUploadedFile for downstream saving.
        
        Raises:
            forms.ValidationError: If any error occurs during image processing.
        
        Returns:
            InMemoryUploadedFile or CloudinaryResource: The processed image file.
        """
        photo = self.cleaned_data.get('photo')

        # Skip processing if the photo is not new (e.g., if it's a CloudinaryResource)
        if photo and not hasattr(photo, 'read'):
            return photo

        if photo:
            # convert image to webp format:
            try:
                # Open the image using PIL
                image = Image.open(photo)
                # Convert to RGB as webp does not support RGBA
                image = image.convert("RGB")
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
        """
        Validate the ReportForm's data and enforce edit permissions.

        - Calls parent clean() to populate `cleaned_data`.
        - If `condition` is 'red' or 'orange', ensures at least one `reason` is selected.
        - If editing an existing report, ensures the current user is either the
          report owner or a superuser; otherwise raises a ValidationError.
        - Adds form errors to the appropriate field or raises a form-level
          ValidationError for permission issues.
        """
        # Call the parent clean method to get cleaned data
        cleaned_data = super().clean()
        # Get the condition, reasons and comments from cleaned data
        condition = cleaned_data.get('condition')
        reasons = cleaned_data.get('reasons')
        comments  = cleaned_data.get('comments')

        # Field‐level validation via add_error()
        if condition in ['red', 'orange'] and not reasons:
            self.add_error(
                'reasons', 
                "At least one reason must be selected when condition is red or orange."
                )
        if condition not in ['red', 'orange'] and reasons:
            self.add_error('reasons',
                "Reasons can only be provided for red or orange conditions."
            )
        if condition == 'white' and not comments:
            self.add_error('comments',
                "Comments must be provided for 'white' condition."
            )
        # Check permissions: allow edit only if the current user is 
        # the original owner or a superuser.
        if self.instance.pk and self.current_user:
            if self.instance.user != self.current_user and not self.current_user.is_superuser:
                raise forms.ValidationError("You do not have permission to edit this report.")

        return cleaned_data


    def handle_delete_photo(self, instance):
        """
        Remove the existing photo from Cloudinary and clear it on the Report instance.

        If the form field `delete_photo` is True and the `instance` has a
        Cloudinary photo resource (with a `public_id`), this method will:
          1. Call `uploader.destroy(public_id, invalidate=True)` to delete the
             image from Cloudinary.
          2. Clear `instance.photo` so the Report no longer references an image.
        
        Any exceptions from the Cloudinary API are caught and logged to the console.

        Args:
            instance (Report): The unsaved Report model instance whose photo
                               should be removed if requested.
        """
        if self.cleaned_data.get('delete_photo') and instance.photo:
            # delete (destroy) CloudinaryResource by public_id
            public_id = getattr(instance.photo, 'public_id', None)
            if public_id:
                try:
                    uploader.destroy(public_id, invalidate=True)
                except CloudinaryError as e:
                    logger.error("Cloudinary error: %s", e)
            instance.photo = None
            print("Deleted existing photo.")


    def save(self, commit=True):
        """
        Save the ReportForm, managing photo deletion and assignment before persisting.

        - Calls super().save(commit=False) to obtain an unsaved Report instance.
        - Uses handle_delete_photo() to remove the existing Cloudinary image if requested.
        - If a new photo was uploaded (in changed_data), assigns it to the instance.
        - If commit=True, saves the instance to the database and handles any m2m relations.

        Args:
            commit (bool): Whether to immediately save the Report instance to the database.

        Returns:
            Report: The Report model instance (saved if commit=True, else unsaved).
        """
        # Get an unsaved instance first
        instance = super().save(commit=False)

        # Delete existing photo if requested
        self.handle_delete_photo(instance)

        # Get the new photo from cleaned_data if one was uploaded
        # and assign it to the instance
        new_photo = self.cleaned_data.get('photo')
        if 'photo' in self.changed_data:
            instance.photo = new_photo

        if commit:
            instance.save()
            self.save_m2m()
        return instance


# SIGNUP FORM
class CustomSignupForm(SignupForm):
    """
    Extends allauth's SignupForm to collect and persist additional user profile data
    during registration:

      - first_name (required)
      - last_name (required)
      - Auto-generates a unique username based on first and last name.
      - is_carer (bool): does the user care for someone who uses a wheeled mobility device?      
      - uses_mobility_device (bool): does the user use a wheeled mobility device?
      - mobility_device_type (str): type of device, if any.

    On save(request):
      1. Creates the User via super().
      2. Normalises and assigns first_name, last_name, and generated username.
      3. Sets the mobility device fields on the user model.
      4. Saves and returns the new User instance.
    """
    first_name = forms.CharField(max_length=30, label="First Name", required=True)
    last_name = forms.CharField(max_length=30, label="Last Name", required=True)

    uses_mobility_device = forms.TypedChoiceField(
        label="Do you use a wheeled mobility device?",
        required=False,
        choices=((False, 'No'),(True, 'Yes')),
        coerce=lambda x: x == 'True',  # converts the posted value to boolean
        widget=forms.Select,
    )

    is_carer = forms.TypedChoiceField(
            label="Do you care for someone who uses a wheeled mobility device?",
            required=False,
            choices=((False, 'No'),(True, 'Yes')),
            coerce=lambda x: x == 'True',  # converts the posted value to boolean
            widget=forms.Select,
    )
    
    # Get the choices defined on the CustomUser model field
    MOBILITY_DEVICE_CHOICES = CustomUser._meta.get_field(
        'mobility_device_type'
    ).choices

    mobility_device_type = forms.ChoiceField(
        label="Please select the primary mobility device that you, or the person you care for, uses:",
        choices=MOBILITY_DEVICE_CHOICES,
        required=False,
    )    

    def __init__(self, *args, **kwargs):
        """
        Initialise the custom signup form with additional profile fields and Crispy styling.

        - Calls the parent SignupForm __init__() to set up default allauth fields.
        - Instantiates a Crispy Forms FormHelper for consistent Bootstrap layout.
        - Sets form_class to 'form-horizontal' for horizontal form styling.
        - Applies responsive grid classes via label_class and field_class
          so labels and inputs align in a two-column layout.
        """
        super().__init__(*args, **kwargs)
        # Create FormHelper for styling
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        # Apply custom classes to labels and fields
        self.helper.label_class = 'col-12 col-sm-4'
        self.helper.field_class = 'col-12 col-sm-8'
        
        # Add a submit button to the form
        from crispy_forms.layout import Submit
        self.helper.add_input(
            Submit(
                name='submit',
                value='Submit',
                css_class='btn btn-mango align-right',
                css_id='signup-submit-btn'
            )
        )

    def clean(self):
        """
        Validate that mobility device fields align with the user's selection.

        - Calls parent clean() to populate cleaned_data.
        - If 'uses_mobility_device' is True, ensures 'mobility_device_type' is provided.
        - Adds a field-specific error if the device type is missing.

        Returns:
            dict: The cleaned_data dictionary.
        """
        cleaned_data = super().clean()
        uses = cleaned_data.get('uses_mobility_device')
        device = cleaned_data.get('mobility_device_type')

        if uses and not device:
            self.add_error('mobility_device_type', "Please select your mobility device type.")
        return cleaned_data

    def save(self, request):
        """
        Create the user account and persist additional profile data.

        - Calls super().save(request) to create the base User object.
        - Normalises first_name and last_name, auto-generates a unique username.
        - Sets uses_mobility_device, mobility_device_type,
          is_carer on the user.
        - Saves and returns the new User instance.

        Args:
            request (HttpRequest): The request object for allauth's signup flow.
        Returns:
            CustomUser: The newly created user profile.
        """
        user_model = get_user_model()  # Get the user model
        user = super().save(request)
        first = self.cleaned_data.get('first_name').strip().lower()
        last = self.cleaned_data.get('last_name').strip().lower()
        base_username = f"{first}_{last}"
        username = base_username

        # Ensure the username is unique
        counter = 1
        while user_model.objects.filter(username=username).exists():
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
    """
    A simple contact-us form for site visitors to send messages or inquiries.

    Fields:
    - first_name (CharField): First name; auto-filled and read-only for authenticated users.
    - last_name  (CharField): Last name; auto-filled and read-only for authenticated users.
    - email      (EmailField): Email address; auto-filled and read-only for authenticated users.
    - message    (CharField): The body of the message or inquiry.

    Behaviour:
    - If a `user` is passed in and is authenticated, the first_name, last_name
        and email fields are pre-populated and locked to prevent editing.
    """
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
        widget=forms.Textarea(attrs={'class': 'form-control', 
                                     'placeholder': 'Your Message', 
                                     'rows': 5}),
        label="Your Message"
    )

    def __init__(self, *args, **kwargs):
        """
        Initialise the ContactForm, applying Bootstrap layout and optional user pre-fill.

        - Removes 'user' from kwargs to check for an authenticated user.
        - Calls the parent __init__() to set up fields.
        - Configures a Crispy Forms FormHelper for horizontal Bootstrap styling.
        - If an authenticated user is provided:
            • Pre-populates 'first_name', 'last_name', and 'email' fields.
            • Marks these fields as readonly to prevent editing.
        """
        user = kwargs.pop('user', None)  # Get the user from the kwargs
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-12 col-sm-4'
        self.helper.field_class = 'col-12 col-sm-8'

        if user and user.is_authenticated:
            # Pre-fill fields with user data and make them read-only
            self.fields['first_name'].initial = user.first_name
            self.fields['first_name'].widget.attrs['readonly'] = True
            self.fields['last_name'].initial = user.last_name
            self.fields['last_name'].widget.attrs['readonly'] = True
            self.fields['email'].initial = user.email
            self.fields['email'].widget.attrs['readonly'] = True

        # Add a submit button to the form
        from crispy_forms.layout import Submit
        self.helper.add_input(
            Submit(
                name='submit',
                value='Send Message',
                css_class='btn btn-mango align-right',
                css_id='contact-submit-btn'
            )
        )

class CustomLoginForm(LoginForm):
    """
    Extends allauth's LoginForm to streamline the login UI and apply Crispy Forms styling:

      - Removes the “Remember Me” option by hiding its field and defaulting it to False.
      - Uses a Crispy Forms FormHelper with:
          • form_tag=False to disable the <form> wrapper,
          • form_class='form-horizontal' for horizontal layout,
          • label_class and field_class for responsive grid styling.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the "Remember Me" field
        self.fields['remember'].widget = forms.HiddenInput()
        self.fields['remember'].initial = False
        self.helper = FormHelper()
        # disable Crispy’s <form> wrapper so we can use our own cubmit button
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-12 col-sm-4'
        self.helper.field_class = 'col-12 col-sm-8'
