from django.contrib import admin
from .models import UnverifiedCompany  # Import UnverifiedCompany
from .models import Company


admin.site.register(UnverifiedCompany)
admin.site.register(Company)

# Register your models here.
