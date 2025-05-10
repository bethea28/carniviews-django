from django.db import models
from company_app.models import Company  # Import the Company model
from django.conf import settings # Import settings for user model
from user_app.models import CustomUser
from django.contrib.postgres.fields import JSONField  # For PostgreSQL
from django.db.models import JSONField  # For other databases (less feature-rich)


from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone

class EditSuggestion(models.Model):
    """
    Model to store user-submitted edit suggestions.
    """
    # The model being edited (Band, Business, or other entity)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_type_label = models.CharField()
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    # The user who made the suggestion
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    # The text of the suggestion
    suggestion_text = models.TextField()

    # The date and time the suggestion was made
    suggested_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Suggestion for {self.content_object} (ID: {self.object_id}) by {self.user}"
