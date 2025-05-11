from django.urls import path
from . import views
from django.urls import include, path

urlpatterns = [
    path('<int:user_id>/<int:company_id>/addBandStory/', views.addBandStory, name='add_band_story'),  # /companies/add/

]