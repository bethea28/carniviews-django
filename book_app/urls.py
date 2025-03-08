from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book, name='book'),
    path('bookPost/', views.bookPost, name='book'),
]