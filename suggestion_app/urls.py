from django.urls import path
from . import views

urlpatterns = [
    path('addEditSuggestion/', views.addEditSuggestion, name='addEditSuggestion'),
    # path('<int:user_id>/<int:entity_id>/addEditSuggestion/', views.addEditSuggestion, name='addEditSuggestion'),

]

