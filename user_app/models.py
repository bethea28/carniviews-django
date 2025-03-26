from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Custom User model to store Google Sign-In information.
    Inherits from AbstractUser for default user fields.
    """
    google_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    photo = models.URLField(null=True, blank=True)
    givenName = models.CharField(max_length=255, null=True, blank=True)
    familyName = models.CharField(max_length=255, null=True, blank=True)
    # email already exists from AbstractUser
    # username already exists from AbstractUser
    # id is the same as google_id
    name = models.CharField(max_length=255, null=True, blank=True) #add name

    # Explicitly set related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_perm_set",
        related_query_name="user",
    )

    def __str__(self):
        if self.name:
          return self.name
        else:
          return self.email

    def save(self, *args, **kwargs):
        # Override save to avoid storing redundant name info.
        if self.givenName and self.familyName:
            self.name = f"{self.givenName} {self.familyName}"
        elif self.givenName:
            self.name = self.givenName
        elif self.familyName:
            self.name = self.familyName

        # If name is still blank, but both given and family are null, set name to email.
        if not self.name and not self.givenName and not self.familyName:
          self.name = self.email

        super().save(*args, **kwargs)

    class Meta:
      verbose_name = "User"
      verbose_name_plural = "Users"