# Generated by Django 5.1.6 on 2025-03-15 13:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassificationReason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classification', models.CharField(choices=[('red', 'Red'), ('orange', 'Orange'), ('green', 'Green'), ('blue', 'Blue')], max_length=6)),
                ('reason', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('classification', models.CharField(choices=[('green', 'Green: Usable and in good condition'), ('orange', 'Orange: Usable but needs improvement'), ('red', 'Red: Dangerous or unusable'), ('blue', 'Blue: Dropped kerb missing or preventing access')], max_length=6)),
                ('comments', models.CharField(blank=True, max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reasons', models.ManyToManyField(blank=True, to='mapper.classificationreason')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='kerb_photos/')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='mapper.report')),
            ],
        ),
    ]
