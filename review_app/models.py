from django.db import models
from company_app.models import Company  # Import the Company model
from django.conf import settings # Import settings for user model
from user_app.models import CustomUser

class Review(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews') # Added user foreign key
    review = models.TextField()
    rating = models.FloatField(default=0.0)
    submitted_by = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Review: '{self.review[:50]}...', Rating: {self.rating}, Company: {self.company.name}, User: {self.user.username}"