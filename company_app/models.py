from django.db import models
import json

class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    hours = models.CharField(max_length=255)
    company_type = models.CharField(max_length=100)
    photos = models.JSONField(default=list)  # Assuming photos is a list of URLs
    hoursData = models.JSONField(default=dict)
    description = models.TextField(blank=True, null=True) #Added description Field


    def __str__(self):
        return self.name

    def get_images(self):
        """Returns all images associated with this company."""
        return self.images.all()  # Access images via the related_name