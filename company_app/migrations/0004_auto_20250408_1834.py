from django.db import migrations
from django.conf import settings
from user_app.models import CustomUser  # Import your CustomUser model
import json

def add_company_data(apps, schema_editor):
    Company = apps.get_model('company_app', 'Company')
    CustomUser = apps.get_model(settings.AUTH_USER_MODEL)

    # --- Example Data ---
    # You'll likely fetch users or create them if needed
    try:
        user1 = CustomUser.objects.get(username='woodymoth@gmail.com')
    except CustomUser.DoesNotExist:
        print("Warning: 'woodymoth@gmail.com' not found. Create a user first or adjust the seed data.")
        return

    try:
        user2 = CustomUser.objects.get(username='bryanbethea28@gmail.com')
    except CustomUser.DoesNotExist:
        print("Warning: 'bryanbethea28@gmail.com' not found. Create a user first or adjust the seed data.")
        return

    Company.objects.create(
        name="Tech Solutions Inc.",
        address="789 Innovation Drive",
        city="New York",
        state="NY",
        zip_code="10002",
        hours="Mon-Fri 9:00 AM - 6:00 PM",
        company_type="Software Development",
        photos=['https://pbs.twimg.com/profile_images/927011857902252032/ykPrO2FN_400x400.jpg'],
        hoursData={'monday': '9-18', 'tuesday': '9-18', 'wednesday': '9-18', 'thursday': '9-18', 'friday': '9-18'},
        description="Developing cutting-edge software solutions.",
        user=user1,
    )

    Company.objects.create(
        name="Green Grocers",
        address="456 Organic Lane",
        city="Brooklyn",
        state="NY",
        zip_code="11201",
        hours="Daily 8:00 AM - 9:00 PM",
        company_type="Grocery Store",
        photos=['https://i1.sndcdn.com/artworks-000208003822-v37o3i-t500x500.jpg'],
        hoursData={'sunday': '8-21', 'monday': '8-21', 'tuesday': '8-21', 'wednesday': '8-21', 'thursday': '8-21', 'friday': '8-21', 'saturday': '8-21'},
        description="Your local source for organic and fresh groceries.",
        user=user2,
    )

    # Add more Company objects here as needed

def remove_company_data(apps, schema_editor):
    Company = apps.get_model('company_app', 'Company')
    Company.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('company_app', '0003_alter_company_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(add_company_data, remove_company_data),
    ]