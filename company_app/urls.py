from django.urls import path
from . import views
from django.urls import include, path

urlpatterns = [
    path('addCompany/', views.addCompany, name='add_company'),  # /companies/add/
    path('getCompanies/', views.getCompanies, name='get_companies'),  
    path('<int:company_id>/addCompanyImage/', include('images_app.urls')), # /companies/<int:company_id>/images/
    path('<int:company_id>/reviews/', include('review_app.urls')), # /companies/<int:company_id>/images/
    # path('<int:company_id>/reviews/', include('review_app.urls')), # /companies/<int:company_id>/images/
    # Add other company-related URLs here (e.g., get company, update company)
]