from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils import timezone
from .models import Business, UnverifiedBusiness
from images_app.models import Image  # Import the Image model
import logging

def verify_business_admin_action(modeladmin, request, queryset):
    """
    Admin action to verify selected unverified businesses.
    """
    for unverified_company in queryset:
        try:
            verified_company = Business(
                name=unverified_company.name,
                address_line1=unverified_company.address_line1,
                address_line2=unverified_company.address_line2,
                city=unverified_company.city,
                region=unverified_company.region,
                postal_code=unverified_company.postal_code,
                country=unverified_company.country,
                hours=unverified_company.hours,
                company_type=unverified_company.company_type,
                photos=unverified_company.photos,
                hoursData=unverified_company.hoursData,
                description=unverified_company.description,
                user=unverified_company.user,
                submitted_at=unverified_company.submitted_at,

                # Newly added fields
                phone=unverified_company.phone,
                email=unverified_company.email,
                facebook=unverified_company.facebook,
                instagram=unverified_company.instagram,
                twitter=unverified_company.twitter,
                website=unverified_company.website,
                id=unverified_company.id
                # contact=unverified_company.contact,
            )
            verified_company.save()

            # Optional: Move associated images from unverified to verified
            # for image in Image.objects.filter(unverified_company=unverified_company):
            #     image.company = verified_company
            #     image.unverified_company = None
            #     image.save()

            unverified_company.delete()
            messages.success(request, f"Company '{verified_company.name}' verified and moved.")
        except Exception as e:
            messages.error(request, f"Error verifying company '{unverified_company.name}': {e}")
            logging.error(f"Error verifying company {unverified_company.id}: {e}", exc_info=True)

verify_business_admin_action.short_description = "Verify selected businesses"

@admin.register(UnverifiedBusiness)
class UnverifiedCompanyAdmin(admin.ModelAdmin):
    actions = [verify_business_admin_action]
    list_display = ['name', 'user', 'submitted_at', 'email', 'phone', 'country',"id"]

@admin.register(Business)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'submitted_at', 'email', 'phone', 'country',"id"]
