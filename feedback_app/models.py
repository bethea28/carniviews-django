from django.db import models
from django.conf import settings # Import settings for user model

class Feedback(models.Model):
    feedback = models.TextField()
