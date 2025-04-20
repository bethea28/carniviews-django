from django.urls import path
from . import views
from django.urls import include, path

urlpatterns = [
    path('<int:user_id>/addVerifiedCompany/', views.addVerifiedCompany, name='add_verified_company'),  # /companies/add/
    path('<int:user_id>/addUnverifiedCompany/', views.addUnverifiedCompany, name='add_unverified_company'),  # /companies/add/
    # path('addCompany/', views.addCompany, name='add_company'),  # /companies/add/
    path('getCompanies/', views.getCompanies, name='get_companies'),  
    path('<int:company_id>/getCompanyRecs/', views.getCompanyRecs, name='get_recommendations'), # /companies/<int:company_id>/images/
    path('<int:user_id>/<int:company_id>/addRec/', views.addRec, name='add_recommendation'), # /companies/<int:company_id>/images/
    path('<int:user_id>/<int:company_id>/addCompanyImages/', include('images_app.urls')), # /companies/<int:company_id>/images/
    path('<int:company_id>/getCompanyImages/', include('images_app.urls')), # /companies/<int:company_id>/images/
    path('<int:company_id>/reviews/', include('review_app.urls')), # /companies/<int:company_id>/images/
    # path('<int:company_id>/reviews/', include('review_app.urls')), # /companies/<int:company_id>/images/
    # Add other company-related URLs here (e.g., get company, update company)
]