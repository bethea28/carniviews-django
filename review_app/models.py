from django.db import models
from company_app.models import Company  # Import the Company model
from django.conf import settings # Import settings for user model
from user_app.models import CustomUser
from django.contrib.postgres.fields import JSONField  # For PostgreSQL
from django.db.models import JSONField  # For other databases (less feature-rich)

class Review(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews') # Added user foreign key
    review = models.TextField()
    music = models.FloatField(default=0.0, null=True)
    service = models.FloatField(default=0.0, null=True)
    vibes = models.FloatField(default=0.0, null=True)
    costume = models.FloatField(default=0.0, null=True)
    price = models.FloatField(default=0.0, null=True)
    food = models.FloatField(default=0.0, null=True)
    value = models.FloatField(default=0.0, null=True)
    amenities = models.FloatField(default=0.0, null=True)
    pickup = models.FloatField(default=0.0, null=True)
    rating = JSONField(default=list, blank=True, null=True)
    review_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Review: '{self.review[:50]}...', Rating: {self.rating}, Company: {self.company.name}, User: {self.user.username}"
    





class RevAgreement(models.Model):
    agreement = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='review_users') #add user foreign key
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='reviews') #add user foreign key
    class Meta:
        db_table = 'review_agreement'
