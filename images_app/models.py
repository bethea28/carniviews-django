from django.db import models
from user_app.models import CustomUser

# Create your models here.
# images_app/models.py
from django.db import models

class Image(models.Model):
    unverified_company = models.ForeignKey('company_app.UnverifiedCompany', on_delete=models.CASCADE, related_name='images')
    # company = models.ForeignKey('company_app.Company', on_delete=models.CASCADE, related_name='images')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='images') # Added user foreign key
    image_url = models.URLField(max_length=1000)  # Or a sufficiently large value
    alt_text = models.CharField(max_length=255, blank=True, null=True) # Optional alt text.

    def __str__(self):
        return self.image_url