from celery import shared_task
from .models import Report

@shared_task
def reverse_geocode_report(report_id):
    """
    Reverse geocode the report's latitude and longitude to get the place name.  
    """
    try:
        report = Report.objects.get(pk=report_id)
    except Report.DoesNotExist:
        return
    report.reverse_geocode(report.latitude, report.longitude)
    report.save(update_fields=["place_name"])
