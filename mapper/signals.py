"""
Signal handlers for the Report model to manage Cloudinary photos.

• delete_photo_on_delete: after a Report is deleted, removes its image from Cloudinary.
• delete_old_photo_on_update: before saving an existing Report, deletes the old image if replaced.
"""
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from cloudinary.uploader import destroy
from .models import Report


@receiver(post_delete, sender=Report)
def delete_photo_on_delete(sender, instance, **kwargs):
    """
    Remove the associated photo from Cloudinary after a Report is deleted.

    This handler listens to Report.post_delete. If the deleted instance
    has a Cloudinary photo resource (with a public_id), it calls `destroy()`
    to delete the image file from Cloudinary storage.
    """
    if instance.photo:
        # Delete the file from Cloudinary
        destroy(instance.photo.public_id)


@receiver(pre_save, sender=Report)
def delete_old_photo_on_update(sender, instance, **kwargs):
    """
    Delete the previous Cloudinary photo before updating a Report instance.

    This handler listens to Report.pre_save. It skips new instances (no PK),
    then fetches the existing record. If the `photo` field is changing
    (old_instance.photo != instance.photo), it calls `destroy()`
    to remove the old image from Cloudinary storage.
    """
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
