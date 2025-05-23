# Generated by Django 4.2.19 on 2025-04-14 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_app', '0005_unverifiedcompany'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unverifiedcompany',
            name='address',
            field=models.CharField(max_length=1255),
        ),
        migrations.AlterField(
            model_name='unverifiedcompany',
            name='name',
            field=models.CharField(max_length=1255),
        ),
        migrations.AlterField(
            model_name='unverifiedcompany',
            name='photos',
            field=models.JSONField(default=dict),
        ),
    ]
