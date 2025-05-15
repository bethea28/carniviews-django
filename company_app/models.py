from django.db import models
import json
from django.conf import settings # Import settings for user model
from user_app.models import CustomUser  # Import the Company model
# from company_app.models import Company

# class Company(models.Model):
#     name = models.CharField(max_length=255)
#     address = models.CharField(max_length=255)
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=50)
#     zip_code = models.CharField(max_length=20)
#     hours = models.CharField(max_length=255)
#     company_type = models.CharField(max_length=100)
#     photos = models.JSONField(default=list)
#     hoursData = models.JSONField(default=dict)
#     description = models.TextField(blank=True, null=True)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='companies') #add user foreign key

class Company(models.Model):
    name = models.CharField(max_length=1255)
    address_line1 = models.CharField(max_length=1255)
    address_line2 = models.CharField(max_length=1255, blank=True, null=True)
    city = models.CharField(max_length=100)
    region = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="State, Province, Region, Parish, etc."  # More general term for regional division
    )
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Zip Code, Postal Code"  # More internationally recognized term
    )
    normalized_country = models.CharField(max_length=100)  # Added field to store the company's country
    country = models.CharField(max_length=100)  # Added field to store the company's country
    hours = models.CharField(max_length=255, blank=True, null=True)
    company_type = models.CharField(max_length=100)
    photos = models.JSONField(default=dict)
    socials =models.JSONField(default=dict)
    contact = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(max_length=255)  # Use URLField
    hoursData = models.JSONField(default=dict)
    claps = models.IntegerField(blank=True, null=True , default=0)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='companies')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_images(self):
        """Returns all images associated with this company."""
        return self.images.all()
    class Meta:
        db_table = 'band_app'


# class UnverifiedCompany(models.Model):
#     name = models.CharField(max_length=1255)
#     address = models.CharField(max_length=1255)
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=50)
#     zip_code = models.CharField(max_length=20)
#     hours = models.CharField(max_length=255)
#     company_type = models.CharField(max_length=100)
#     # photos = models.JSONField(null=True, blank=True)
#     photos = models.JSONField(default=dict)  # Correct way for mutable defaults
#     hoursData = models.JSONField(default=dict)
#     description = models.TextField(blank=True, null=True)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='unverified_companies') #add user foreign key
#     submitted_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Unverified: {self.name} (Submitted by {self.user})"



class UnverifiedCompany(models.Model):
    name = models.CharField(max_length=1255)
    address_line1 = models.CharField(max_length=1255)
    address_line2 = models.CharField(max_length=1255, blank=True, null=True)
    city = models.CharField(max_length=100)
    region = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="State, Province, Region, Parish, etc."  # More general term for regional division
    )
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Zip Code, Postal Code"  # More internationally recognized term
    )
    normalized_country = models.CharField(max_length=100)  # Added field to store the company's country
    country = models.CharField(max_length=100)  # Added field to store the company's country
    hours = models.CharField(max_length=255, blank=True, null=True)
    contact = models.CharField(max_length=255, blank=True, null=True)
    company_type = models.CharField(max_length=100)
    claps = models.IntegerField(blank=True, null=True, default=0)
    socials =models.JSONField(default=dict)
    photos = models.JSONField(default=dict)
    website = models.URLField(max_length=255)  # Use URLField
    hoursData = models.JSONField(default=dict)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='unverified_companies')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Unverified: {self.name} (Submitted by {self.user})"
    
    class Meta:
        db_table = 'unverifiedband_app'


class Recommendation(models.Model):
    rec = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='users') #add user foreign key
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='companies') #add user foreign key
    class Meta:
        db_table = 'band_recommendation'
