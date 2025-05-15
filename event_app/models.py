from django.db import models
from django.conf import settings # Import settings to reference the user model
from user_app.models import CustomUser  # Import your CustomUser model

# class Event(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='events')  # Use CustomUser directly
#     name = models.CharField(max_length=255)
#     address = models.CharField(max_length=255)
#     price = models.CharField(max_length=100)
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=50)
#     zip_code = models.CharField(max_length=20)
#     hours = models.JSONField(default=dict, blank=True, null=True)  # Store hours data as JSON
#     start_time = models.CharField(max_length=50)
#     end_time = models.CharField(max_length=50)
#     type = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#     # allImages = models.ManyToManyField('EventImage', blank=True) # Removed EventImage model and using ImageField directly
    
#     def __str__(self):
#         return self.name


class Event(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='events')  # Use CustomUser directly
    name = models.CharField(max_length=255)
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
    claps = models.IntegerField(blank=True, null=True, default=0)
    country = models.CharField(max_length=100)  # Added field to store the company's country
    price = models.CharField(max_length=100)
    date = models.CharField(max_length=50)
    photos = models.JSONField(default=dict)
    start_time = models.CharField(max_length=50)
    end_time = models.CharField(max_length=50)
    type = models.CharField(max_length=255)
    ticket = models.URLField(max_length=255)  # Use URLField
    description = models.TextField(blank=True, null=True)
    # allImages = models.ManyToManyField('EventImage', blank=True) # Removed EventImage model and using ImageField directly
    
    def __str__(self):
        return self.name

class EventImage(models.Model):  #added
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
    image =  models.JSONField(default=dict, blank=True, null=True)
