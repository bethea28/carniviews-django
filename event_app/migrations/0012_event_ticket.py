# Generated by Django 4.2.19 on 2025-04-19 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0011_remove_event_address_remove_event_hours_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='ticket',
            field=models.URLField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
