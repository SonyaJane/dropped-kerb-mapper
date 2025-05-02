from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch import receiver
from cloudinary.uploader import destroy
from .models import Report
from .tasks import reverse_geocode_report
from django.utils import timezone


@receiver(post_delete, sender=Report)
def delete_photo_on_delete(sender, instance, **kwargs):
    if instance.photo:
        # Delete the file from Cloudinary
        destroy(instance.photo.public_id)


@receiver(pre_save, sender=Report)
def delete_old_photo_on_update(sender, instance, **kwargs):
    if not instance.pk:
        # If the instance is new, do nothing
        return

    try:
        old_instance = Report.objects.get(pk=instance.pk)
    except Report.DoesNotExist:
        return

    # If the photo is being updated, delete the old file
    if old_instance.photo and old_instance.photo != instance.photo:
        destroy(old_instance.photo.public_id)


@receiver(post_save, sender=Report)
def schedule_geocode(sender, instance, created, **kwargs):
    now = timezone.now()

    # Retry for any reports whose retry time has passed
    pending = Report.objects.filter(
        geocode_retry_at__isnull=False,
        geocode_retry_at__lte=now
    )
    for rpt in pending:
        reverse_geocode_report.delay(rpt.pk)
