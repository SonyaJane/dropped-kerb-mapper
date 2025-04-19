import django_tables2 as tables
from .models import Report

class ReportTable(tables.Table):
    class Meta:
        model = Report
        fields = (
            'id',
            'user',
            'user_report_number',
            'latitude',
            'longitude',
            'place_name',
            'county',
            'local_authority',
            'condition',
            'reasons',
            'comments',
            'photo',
            'created_at',
            'updated_at')