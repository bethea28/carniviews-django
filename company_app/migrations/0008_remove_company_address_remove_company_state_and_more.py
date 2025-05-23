# Generated by Django 4.2.19 on 2025-04-18 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_app', '0007_rename_address_unverifiedcompany_address_line1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='address',
        ),
        migrations.RemoveField(
            model_name='company',
            name='state',
        ),
        migrations.RemoveField(
            model_name='company',
            name='zip_code',
        ),
        migrations.AddField(
            model_name='company',
            name='address_line1',
            field=models.CharField(default='', max_length=1255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='address_line2',
            field=models.CharField(blank=True, max_length=1255, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='country',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='postal_code',
            field=models.CharField(blank=True, help_text='Zip Code, Postal Code', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='region',
            field=models.CharField(blank=True, help_text='State, Province, Region, Parish, etc.', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='hours',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=1255),
        ),
        migrations.AlterField(
            model_name='company',
            name='photos',
            field=models.JSONField(default=dict),
        ),
    ]
