from django.contrib.gis.db import models as geomodels
from django.db import models
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from multiselectfield import MultiSelectField
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from geopy import Nominatim
from django.conf import settings

class CustomUser(AbstractUser):
    # Add mobility device fields
    uses_mobility_device = models.BooleanField(
        default=False,
        verbose_name="Uses a wheeled mobility device"
    )
    MOBILITY_DEVICE_CHOICES = (
        ('manual_wheelchair', 'Manual Wheelchair'),
        ('powered_wheelchair', 'Powered Wheelchair'),
        ('mobility_scooter', 'Mobility Scooter'),
        ('tricycle', 'Tricycle'),
        ('adapted_bicycle', 'Adapted Bicycle'),
        ('bicycle', 'Bicycle'),
        ('other', 'Other'),
    )
    mobility_device_type = models.CharField(
        max_length=50,
        choices=MOBILITY_DEVICE_CHOICES,
        blank=True,
        null=True,
        verbose_name="Mobility Device Type"
    )
    
class County(geomodels.Model):
    county = models.CharField(max_length=100)
    polygon = geomodels.MultiPolygonField(srid=4326)  # stores the county geometry, target CRS is WGS84 (lat/long)

    class Meta:
        verbose_name_plural = "Counties"  # Set the plural name to "Counties"
        
    def __str__(self):
        return self.county
    
    
class LocalAuthority(geomodels.Model):
    local_authority = models.CharField(max_length=100)
    polygon = geomodels.MultiPolygonField(srid=4326)  # stores the county geometry, target CRS is WGS84 (lat/long)

    class Meta:
        verbose_name_plural = "LocalAuthorities"
        
    def __str__(self):
        return self.local_authority

class Report(models.Model):
    TRAFFIC_LIGHT_CHOICES = [
        ('green', 'Green'),   # Usable and in good condition
        ('orange', 'Orange'), # Usable but needs improvement
        ('red', 'Red'),       # Dangerous or unusable
        ('blue', 'Blue'),     # Dropped kerb missing or preventing access
    ]
    
    ALLOWED_REASONS = [
        ('steep_gradient', 'Steep gradient'),
        ('lip_too_high', 'Lip too high'),
        ('cobbles', 'Cobblestones'),
        ('obstacle', 'Obstacle'),
        ('no_visual_marking', 'No visual marking'),
        ('no_tactile_paving', 'No tactile paving'),
        ('narrow_pavement', 'Narrow pavement'),
        ('uneven_road_surface', 'Uneven road surface'),
        ('uneven_pavement_surface', 'Uneven pavement surface'),
        ('tight_turning_circle', 'Tight turning circle'),
        ('incorrectly_angled', 'Incorrectly angled'),
        ('broken_road_surface', 'Broken road surface'),
        ('broken_pavement_surface', 'Broken pavement surface'),
        ('accessibility_barrier', 'Accessibility barrier'),
    ]
    
    # Unique report number for each user
    user_report_number = models.PositiveIntegerField(null=True, blank=True)  
    # Store location as latitude and longitude
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    # ForeignKey to the matching County
    county = models.ForeignKey(County, null=True, blank=True, on_delete=models.SET_NULL)
    local_authority = models.ForeignKey(LocalAuthority, null=True, blank=True, on_delete=models.SET_NULL)
    # place name (get via reverse geocoding)
    place_name = models.CharField(max_length=1000, blank=True, null=True)
    # Uses a choices field to enforce the available traffic light ratings.
    condition = models.CharField(max_length=6, choices=TRAFFIC_LIGHT_CHOICES)
    
    # Each instance represents an option (checkbox) that explains why a particular 
    # traffic light condition was chosen. 
    reasons = MultiSelectField(choices=ALLOWED_REASONS, blank=True, null=True)
    comments = models.CharField(max_length=1000, blank=True) # Optional comments
    
    photo = CloudinaryField('image', blank=True, null=True) # Optional photo of the dropped kerb
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # custom user model
        on_delete=models.SET_NULL,
        related_name='reports',
        null=True,  # Allow the user field to be NULL
        blank=True 
    )
    
    username = models.CharField(max_length=150, blank=True, null=True)  # Store the username as a string
    
    class Meta:
        ordering = ['-created_at'] # Sort reports by creation date, newest first.
        verbose_name = "Dropped Kerb Report" # Singular name for the model in the admin interface.
        verbose_name_plural = "Dropped Kerb Reports" # Plural name for the model in the admin interface.
        get_latest_by = "created_at" # Retrieve the latest report by creation date.
        indexes = [
            models.Index(fields=['condition']), # Index the condition field for faster lookups.
            models.Index(fields=['user']),      # Index the user field for faster lookups.
        ]
        
    def clean(self):
        """
        Enforce that reasons are only provided if the condition is red or orange.
        """
        super().clean()
        if self.condition not in ['red', 'orange'] and self.reasons:
            raise ValidationError("Reasons can only be provided for red or orange conditions.")
 
    def save(self, *args, **kwargs):
        # Automatically assign the next report number for the user
        if self.user and not self.user_report_number:
            # Get the highest report number for this user and increment it
            last_report = Report.objects.filter(user=self.user).order_by('-user_report_number').first()
            self.user_report_number = (last_report.user_report_number + 1) if last_report else 1
        # If latitude and longitude are provided, create a GeoDjango Point.
        if self.latitude and self.longitude:
            lon = round(self.longitude, 6)
            lat = round(self.latitude, 6)
            point = Point((lon, lat))  # Ensure the point is in the same CRS as your County model.
            # Find the first County whose polygon contains the point.
            # Ensure the County data is in the same CRS, here EPSG:4326.
            matching_county = County.objects.filter(polygon__contains=point).first()
            if matching_county:
                self.county = matching_county
            else:
                self.county = None  # Or handle cases where no county matches.
            # find the matching local authority
            matching_local_authority = LocalAuthority.objects.filter(polygon__contains=point).first()
            if matching_local_authority:
                self.local_authority = matching_local_authority
            else:
                self.local_authority = None
            # Reverse geocode the latitude and longitude to get the place name.
            geolocator = Nominatim(user_agent="Dropped-Kerb-Mapper")
            location = geolocator.reverse(f"{lat},{lon}", zoom=17, addressdetails=True)
            # Extract all values from location.raw['address'] until the key 'county'
            address = location.raw.get('address', {})
            values_until_county = []
            for key, value in address.items():
                if key in ['county', 'state', 'country', 'postode', 'country_code', 'province'] or key.startswith('ISO'):
                    break
                if value not in values_until_county:
                    # Avoid duplicates in the place name
                    values_until_county.append(value)
            # Join the values into a single string
            self.place_name = ", ".join(values_until_county) if values_until_county else None
            # Automatically set the username field if the user is set
            if self.user and not self.username:
                self.username = self.user.username
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Report {self.id}: {self.condition} by {self.username or 'Unknown User'}"