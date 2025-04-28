from django.urls import path
from . import views

urlpatterns = [
    path('<int:user_id>/addEvent/', views.addEvent, name='addEvent'),
        # path('<int:user_id>/addVerifiedCompany/', views.addVerifiedCompany, name='add_verified_company'),  # /companies/add/

    path('<str:country>/getAllEvents/', views.getAllEvents, name='getAllEvents'),
   
]