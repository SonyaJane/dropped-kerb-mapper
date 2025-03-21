# Generated by Django 5.1.6 on 2025-03-18 18:12

import django.utils.timezone
import multiselectfield.db.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapper', '0003_remove_report_reasons_delete_classificationreason_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photo',
            options={'ordering': ['-created_at'], 'verbose_name': 'Dropped Kerb Photo', 'verbose_name_plural': 'Dropped Kerb Photos'},
        ),
        migrations.AlterModelOptions(
            name='report',
            options={'get_latest_by': 'created_at', 'ordering': ['-created_at'], 'verbose_name': 'Dropped Kerb Report', 'verbose_name_plural': 'Dropped Kerb Reports'},
        ),
        migrations.AddField(
            model_name='photo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='report',
            name='reasons',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('too_steep', 'Too steep'), ('lip_too_high', 'Lip too high'), ('cobbles', 'Cobblestones'), ('obstacle', 'Obstacle'), ('no-visual_indication', 'No visual indication'), ('narrow_pavement', 'Narrow pavement'), ('uneven_ground', 'Uneven ground'), ('turning_circle_too_tight', 'Turning circle too tight'), ('incorrectly_angled', 'Incorrectly angled'), ('broken_road_surface', 'Broken road surface'), ('broken_pavement surface', 'Broken pavement surface'), ('accessibility_barrier', 'Accessibility barrier')], help_text='Select reasons (allowed only if classification is red or orange)', max_length=200, null=True),
        ),
        migrations.AddIndex(
            model_name='photo',
            index=models.Index(fields=['report'], name='mapper_phot_report__cf78d3_idx'),
        ),
        migrations.AddIndex(
            model_name='report',
            index=models.Index(fields=['classification'], name='mapper_repo_classif_843e11_idx'),
        ),
        migrations.AddIndex(
            model_name='report',
            index=models.Index(fields=['user'], name='mapper_repo_user_id_dff4be_idx'),
        ),
    ]
