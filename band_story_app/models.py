from django.db import models
from django.conf import settings # Import settings to reference the user model
from user_app.models import CustomUser  # Import your CustomUser model
from company_app.models import Company  # Import the Company model

class BandStory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='band_stories')  # Use CustomUser directly
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='band_stories')  # New company field
    name = models.CharField(max_length=255)
    intro = models.TextField(blank=True, null=True)
    vibe = models.TextField(blank=True, null=True)
    costume = models.TextField(blank=True, null=True)
    moments = models.TextField(blank=True, null=True)
    reflection = models.TextField(blank=True, null=True)
    photos = models.JSONField(default=dict)

    # allImages = models.ManyToManyField('EventImage', blank=True) # Removed EventImage model and using ImageField directly
    
    def __str__(self):
        return self.name

