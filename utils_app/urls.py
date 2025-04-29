from django.urls import path
from . import views

urlpatterns = [
        # path('<int:user_id>/addVerifiedCompany/', views.addVerifiedCompany, name='add_verified_company'),  # /companies/add/

    path('duplicationCheck/', views.duplicationCheck, name='duplication_check'),
   
]