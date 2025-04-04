from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from multiselectfield import MultiSelectField
from cloudinary.models import CloudinaryField

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
    
    # Store location as latitude and longitude
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    # Uses a choices field to enforce the available traffic light ratings.
    classification = models.CharField(max_length=6, choices=TRAFFIC_LIGHT_CHOICES)
    
    # Each instance represents an option (checkbox) that explains why a particular 
    # traffic light classification was chosen. 
    reasons = MultiSelectField(choices=ALLOWED_REASONS, blank=True, null=True, help_text="Select reasons (allowed only if classification is red or orange)")
    comments = models.CharField(max_length=1000, blank=True) # Optional comments
    
    photo = CloudinaryField('image', blank=True, null=True) # Optional photo of the dropped kerb
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # A foreign key to associate the report with the authenticated user who submitted it.
    # on_delete the report is retained, but its user field will be set to null.
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reports")

    class Meta:
        ordering = ['-created_at'] # Sort reports by creation date, newest first.
        verbose_name = "Dropped Kerb Report" # Singular name for the model in the admin interface.
        verbose_name_plural = "Dropped Kerb Reports" # Plural name for the model in the admin interface.
        get_latest_by = "created_at" # Retrieve the latest report by creation date.
        indexes = [
            models.Index(fields=['classification']), # Index the classification field for faster lookups.
            models.Index(fields=['user']),           # Index the user field for faster lookups.
        ]
        
    def clean(self):
        """
        Enforce that reasons are only provided if the classification is red or orange.
        """
        super().clean()
        if self.classification not in ['red', 'orange'] and self.reasons:
            raise ValidationError("Reasons can only be provided for red or orange classifications.")
 
    def __str__(self):
        return f"Report {self.id}: {self.classification} by {self.user}"
 