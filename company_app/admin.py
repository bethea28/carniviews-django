from django.contrib import admin
from .models import UnverifiedCompany  # Import UnverifiedCompany
from .models import Company

# Register your models here.
from django.urls import reverse
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils import timezone
from images_app.models import Image # Import the Image model

def verify_company_admin_action(modeladmin, request, queryset):
    """
    Admin action to verify selected unverified companies.
    """
    for unverified_company in queryset:
        try:
            # Create a new Company instance with data from UnverifiedCompany
            verified_company = Company(
                name=unverified_company.name,
                address_line1=unverified_company.address_line1,
                address_line2=unverified_company.address_line2,
                city=unverified_company.city,
                region=unverified_company.region,
                postal_code=unverified_company.postal_code,
                country=unverified_company.country,
                hours=unverified_company.hours,
                company_type=unverified_company.company_type,
                photos=unverified_company.photos,  # Copy the photos JSON data
                hoursData=unverified_company.hoursData,
                description=unverified_company.description,
                user=unverified_company.user,  # Keep the same user
                submitted_at=unverified_company.submitted_at, #copy submitted at
                # verified_at=timezone.now(),  # Set the verification timestamp
            )
            verified_company.save()  # Save the new Company instance

            # Handle images:  Move associated images to the verified company
            # for image in Image.objects.filter(unverified_company=unverified_company):
            #     image.company = verified_company  # Change the foreign key
            #     image.unverified_company = None  # Clear the old foreign key
            #     image.save()

            # Delete the UnverifiedCompany instance
            unverified_company.delete()

            messages.success(request, f"Company '{verified_company.name}' verified and moved.")
        except Exception as e:
            messages.error(request, f"Error verifying company '{unverified_company.name}': {e}")
            # It's good to log the error for debugging
            import logging
            logging.error(f"Error verifying company {unverified_company.id}: {e}", exc_info=True)

    verify_company_admin_action.short_description = "Verify selected companies"  # Set description for the action

@admin.register(UnverifiedCompany)
class UnverifiedCompanyAdmin(admin.ModelAdmin):
    # ... your other admin configurations ...
    actions = [verify_company_admin_action]  # Add the action here
    list_display = ['name', 'user', 'submitted_at']
    # Removed the verify_link,  admin actions are the preferred way to do this in the admin

@admin.register(Company)  # Register the Verified Company model
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'submitted_at']
    # ... your admin configurations for verified companies



# admin.site.register(UnverifiedCompany)
# admin.site.register(Company)
