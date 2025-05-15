from django.db import models
from django.conf import settings # Import settings for user model
from user_app.models import CustomUser  # Import the Company model
# from company_app.models import Company


class Business(models.Model):
    name = models.CharField(max_length=1255)
    address_line1 = models.CharField(max_length=1255)
    address_line2 = models.CharField(max_length=1255, blank=True, null=True)
    city = models.CharField(max_length=100)
    region = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="State, Province, Region, Parish, etc."
    )
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Zip Code, Postal Code"
    )
    claps = models.IntegerField(blank=True, null=True, default=0)
    country = models.CharField(max_length=100)
    hours = models.CharField(max_length=255, blank=True, null=True)
    company_type = models.CharField(max_length=100)
    photos = models.JSONField(default=dict)
    hoursData = models.JSONField(default=dict)
    description = models.TextField(blank=True, null=True)

    # New fields
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=100, blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    facebook = models.CharField(max_length=100, blank=True, null=True)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='verified_business_app_user')
    submitted_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

    def get_images(self):
        """Returns all images associated with this company."""
        return self.images.all()


class UnverifiedBusiness(models.Model):
    name = models.CharField(max_length=1255)
    address_line1 = models.CharField(max_length=1255)
    address_line2 = models.CharField(max_length=1255, blank=True, null=True)
    city = models.CharField(max_length=100)
    region = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="State, Province, Region, Parish, etc."
    )
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Zip Code, Postal Code"
    )
    claps = models.IntegerField(blank=True, null=True, default=0)
    country = models.CharField(max_length=100)
    hours = models.CharField(max_length=255, blank=True, null=True)
    company_type = models.CharField(max_length=100)
    photos = models.JSONField(default=dict)
    hoursData = models.JSONField(default=dict)
    description = models.TextField(blank=True, null=True)

    # New fields
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=100, blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    facebook = models.CharField(max_length=100, blank=True, null=True)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='unverified_business_app_user')
    submitted_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

    def get_images(self):
        """Returns all images associated with this company."""
        return self.images.all()


# class UnverifiedCompany(models.Model):
#     name = models.CharField(max_length=1255)
#     address_line1 = models.CharField(max_length=1255)
#     address_line2 = models.CharField(max_length=1255, blank=True, null=True)
#     city = models.CharField(max_length=100)
#     region = models.CharField(
#         max_length=100,
#         blank=True,
#         null=True,
#         help_text="State, Province, Region, Parish, etc."  # More general term for regional division
#     )
#     postal_code = models.CharField(
#         max_length=20,
#         blank=True,
#         null=True,
#         help_text="Zip Code, Postal Code"  # More internationally recognized term
#     )
#     country = models.CharField(max_length=100)  # Added field to store the company's country
#     hours = models.CharField(max_length=255, blank=True, null=True)
#     contact = models.CharField(max_length=255, blank=True, null=True)
#     business_type = models.CharField(max_length=100)
#     photos = models.JSONField(default=dict)
#     website = models.URLField(max_length=255)  # Use URLField
#     hoursData = models.JSONField(default=dict)
#     description = models.TextField(blank=True, null=True)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_business_app')
#     submitted_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Unverified: {self.name} (Submitted by {self.user})"
    
#     class Meta:
#         db_table = 'unverifiedband_app'


# class Recommendation(models.Model):
#     rec = models.CharField(max_length=255)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='users') #add user foreign key
#     business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='business') #add user foreign key
