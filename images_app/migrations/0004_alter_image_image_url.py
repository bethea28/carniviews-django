# Generated by Django 4.2.19 on 2025-04-13 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images_app', '0003_remove_image_company_image_unverified_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_url',
            field=models.URLField(max_length=1000),
        ),
    ]
