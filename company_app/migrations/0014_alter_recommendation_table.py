# Generated by Django 4.2.19 on 2025-04-25 03:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company_app', '0013_alter_company_table_alter_unverifiedcompany_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='recommendation',
            table='band_recommendation',
        ),
    ]
