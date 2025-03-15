from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Each instance represents an option (checkbox) that explains why a particular 
# traffic light classification was chosen. The classification field helps link 
# each reason to the corresponding traffic light category. This lets us define 
# different sets of reasons for each classification.
class ClassificationReason(models.Model):
    CLASSIFICATION_CHOICES = [
        ('red', 'Red'),
        ('orange', 'Orange'),
        ('green', 'Green'),
        ('blue', 'Blue'),
    ]
    classification = models.CharField(max_length=6, choices=CLASSIFICATION_CHOICES)
    # prepopulate this table with the allowable reasons for each classification.
    reason = models.CharField(max_length=255)

    def __str__(self):
        return self.reason

    
class Report(models.Model):
    TRAFFIC_LIGHT_CHOICES = [
        ('green', 'Green: Usable and in good condition'),
        ('orange', 'Orange: Usable but needs improvement'),
        ('red', 'Red: Dangerous or unusable'),
        ('blue', 'Blue: Dropped kerb missing or preventing access'),
    ]
    
    # Store location as latitude and longitude
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    # Uses a choices field to enforce the available traffic light ratings.
    classification = models.CharField(max_length=6, choices=TRAFFIC_LIGHT_CHOICES)
    
    # A many-to-many field links to ClassificationReason so that multiple reasons can be associated with a single report.
    # When building the form we can filter the queryset for reasons so that only options matching the chosen classification are displayed.
    reasons = models.ManyToManyField(ClassificationReason, blank=True)
    comments = models.CharField(max_length=1000, blank=True) # Optional comments
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # A foreign key to associate the report with the authenticated user who submitted it.
    # on_delete the report is retained, but its user field will be set to null.
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reports")

    def clean(self):
        """
        Enforce that reasons can only be provided for red or orange classifications.
        For green or blue, no reasons should be selected (comments can be added).
        """
        super().clean()

        if self.classification not in ['red', 'orange']:
            if self.reasons.exists():
                raise ValidationError("Reasons can only be provided for red or orange classifications.")
 
    def __str__(self):
        return f"{self.get_classification_display()} report by {self.user}"



# A single report can have multiple photos attached
# stores individual photos. Each photo is linked to a report using a ForeignKey.
# The photo field is an ImageField that stores the uploaded image in the kerb_photos/ directory.
# The __str__ method returns a string representation of the photo, including the report ID.
class Photo(models.Model):
    # ForeignKey linking each photo to a particular Report
    # on_delete=models.CASCADE ensures that if a report is deleted, all associated photos are also deleted.
    # related_name="photos" allows you to access all photos for a report using report.photos.all().
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="photos")
    photo = models.ImageField(upload_to='kerb_photos/')
    
    def __str__(self):
        return f"Photo for Report {self.report.id}"

