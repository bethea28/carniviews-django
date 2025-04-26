from django.urls import path
from . import views
from django.urls import include, path

urlpatterns = [
    path('getBusinesses/', views.getBusinesses, name='get_business'),  # /companies/add/
    path('<int:user_id>/addBusiness/', views.addBusiness, name='add_business'),  # /companies/add/
]