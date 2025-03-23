# Generated by Django 5.1.6 on 2025-03-19 18:46

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapper', '0005_alter_report_classification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='reasons',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('steep_gradient', 'Steep gradient'), ('lip_too_high', 'Lip too high'), ('cobbles', 'Cobblestones'), ('obstacle', 'Obstacle'), ('no_visual_marking', 'No visual marking'), ('no_tactile_paving', 'No tactile paving'), ('narrow_pavement', 'Narrow pavement'), ('uneven_road_surface', 'Uneven road surface'), ('uneven_pavement_surface', 'Uneven pavement surface'), ('tight_turning_circle', 'Tight turning circle'), ('incorrectly_angled', 'Incorrectly angled'), ('broken_road_surface', 'Broken road surface'), ('broken_pavement_surface', 'Broken pavement surface'), ('accessibility_barrier', 'Accessibility barrier')], help_text='Select reasons (allowed only if classification is red or orange)', max_length=246, null=True),
        ),
    ]
