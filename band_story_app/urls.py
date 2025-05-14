from django.urls import path
from . import views
from django.urls import include, path

urlpatterns = [
    path('addBandStory/', views.addBandStory, name='add_band_story'),  # /companies/add/
    path('<company_id>/getBandStories/', views.getBandStories, name='get_band_story'),  # /companies/add/

]