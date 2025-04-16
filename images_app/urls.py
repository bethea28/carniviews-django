from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.addCompanyImages, name='addCompanyImages'),
    path('get/', views.getCompanyImages, name='getCompanyImages'),
   
]