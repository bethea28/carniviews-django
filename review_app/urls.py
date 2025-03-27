from django.urls import path
from . import views

urlpatterns = [
    path('addReview/', views.addReview, name='addReview'),
    path('getReviews/', views.getReviews, name='getReviews'),
    path('getRatings/', views.getRatings, name='getRating'),
    path('<int:user_id>/<int:company_id>/addReview/', views.addReview, name='addReview'),
   
]

    # path('<int:company_id>/addReview/', include('review_app.urls')), # /companies/<int:company_id>/images/
