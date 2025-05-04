from django.urls import path
from . import views
from django.urls import include, path

urlpatterns = [
    path('<str:country>/getBusinesses/', views.getBusinesses, name='get_business'),  # /companies/add/
    path('<int:user_id>/addBusiness/', views.addBusiness, name='add_business'),  # /companies/add/
    path('<int:user_id>/addUnverifiedBusiness/', views.addUnverifiedBusiness, name='add_unverified_business'),  # /companies/add/
    path('<int:biz_id>/editVerifiedBusiness/', views.editVerifiedBusiness, name='edit_verified_business'),  # /companies/add/
]