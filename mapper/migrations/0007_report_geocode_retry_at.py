# Generated by Django 5.2 on 2025-05-02 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapper', '0006_alter_report_condition'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='geocode_retry_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
