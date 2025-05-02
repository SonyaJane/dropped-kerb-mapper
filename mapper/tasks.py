from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from .models import Report

@shared_task(bind=True, max_retries=3, default_retry_delay=3600)
def reverse_geocode_report(self, report_id):
    try:
        report = Report.objects.get(pk=report_id)
    except Report.DoesNotExist:
        return

    success = report._reverse_geocode(report.latitude, report.longitude)
    if not success:
        # schedule another retry in 1 hour
        report.geocode_retry_at = timezone.now() + timedelta(hours=1)
        report.save(update_fields=["geocode_retry_at"])
        try:
            raise Exception("Reverse geocode failed, retrying")
        except Exception as exc:
            self.retry(exc=exc)
    else:
        # clear retry flag on success
        report.geocode_retry_at = None
        report.save(update_fields=["place_name", "geocode_retry_at"])
        