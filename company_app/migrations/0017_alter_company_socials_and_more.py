# Generated by Django 4.2.19 on 2025-04-28 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_app', '0016_company_socials_unverifiedcompany_socials'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='socials',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='unverifiedcompany',
            name='socials',
            field=models.JSONField(default=list),
        ),
    ]
