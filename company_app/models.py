from django.db import models
import json
from images_app.models import Image  # Import the Image model

class Company(models.Model):
    companyInfo = models.TextField(default='{}')  # Store companyInfo as JSON object
    hoursData = models.TextField(default='{}')  # Store hoursData as JSON object

    def set_companyInfo(self, info_dict):
        """Sets the companyInfo field from a Python dictionary."""
        self.companyInfo = json.dumps(info_dict)

    def get_companyInfo(self):
        """Returns the companyInfo field as a Python dictionary."""
        try:
            return json.loads(self.companyInfo)
        except json.JSONDecodeError:
            return {}

    def set_hoursData(self, hours_dict):
        """Sets the hoursData field from a Python dictionary."""
        self.hoursData = json.dumps(hours_dict)

    def get_hoursData(self):
        """Returns the hoursData field as a Python dictionary."""
        try:
            return json.loads(self.hoursData)
        except json.JSONDecodeError:
            return {}

    def save(self, *args, **kwargs):
        """Override save to ensure all JSON fields are valid."""
        try:
            json.loads(self.companyInfo)
        except json.JSONDecodeError:
            self.companyInfo = '{}'

        try:
            json.loads(self.hoursData)
        except json.JSONDecodeError:
            self.hoursData = '{}'
        super().save(*args, **kwargs)

    def get_images(self):
        """Returns all images associated with this company."""
        return self.images.all()  # Access images via the related_name