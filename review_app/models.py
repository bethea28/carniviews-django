from django.db import models

class Review(models.Model):
  review = models.CharField(max_length=255)
  rating = models.FloatField(default=0.0)  # Set the default rating to 0.0
