# Generated by Django 4.2.19 on 2025-04-29 23:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0012_event_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='date',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]
