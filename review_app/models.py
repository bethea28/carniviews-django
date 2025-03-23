from django.db import models
from company_app.models import Company  # Import the Company model

class Review(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='reviews') # Added company foreign key
    review = models.TextField()
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"Review: '{self.review[:50]}...', Rating: {self.rating}, Company: {self.company.name}"