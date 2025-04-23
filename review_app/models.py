from django.db import models
from company_app.models import Company  # Import the Company model
from django.conf import settings # Import settings for user model
from user_app.models import CustomUser

class Review(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews') # Added user foreign key
    review = models.TextField()
    submitted_by = models.TextField()
    music = models.FloatField(default=0.0)
    service = models.FloatField(default=0.0)
    vibes = models.FloatField(default=0.0)
    costume = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)
    food = models.FloatField(default=0.0)
    value = models.FloatField(default=0.0)
    amenities = models.FloatField(default=0.0)
    pickup = models.FloatField(default=0.0)
    rating = models.FloatField(default=0.0)
    review_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Review: '{self.review[:50]}...', Rating: {self.rating}, Company: {self.company.name}, User: {self.user.username}"