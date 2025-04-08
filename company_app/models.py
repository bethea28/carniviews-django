from django.db import models
import json
from django.conf import settings # Import settings for user model
from user_app.models import CustomUser  # Import the Company model


class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    hours = models.CharField(max_length=255)
    company_type = models.CharField(max_length=100)
    photos = models.JSONField(default=list)
    hoursData = models.JSONField(default=dict)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='companies') #add user foreign key

    def __str__(self):
        return self.name

    def get_images(self):
        """Returns all images associated with this company."""
        return self.images.all()
    

    from django.db import models

class UnverifiedCompany(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    hours = models.CharField(max_length=255)
    company_type = models.CharField(max_length=100)
    photos = models.JSONField(default=list)
    hoursData = models.JSONField(default=dict)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='unverified_companies') #add user foreign key
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Unverified: {self.name} (Submitted by {self.user})"