from django.urls import path
from . import views

urlpatterns = [
    # path('addReview/', views.addReview, name='addReview'),
    path('<int:company_id>/getReviews/', views.getReviews, name='getReviews'),
    path('<int:company_id>/getReviewAvgs/', views.getReviewAvgs, name='getReviewAvgs'),
    path('getRatings/', views.getRatings, name='getRating'),
    path('<int:user_id>/<int:company_id>/addReview/', views.addReview, name='addReview'),
    path('addRevAgreement/', views.addRevAgreement, name='add_revagreement'), # /companies/<int:company_id>/images/

]

    # path('<int:company_id>/addReview/', include('review_app.urls')), # /companies/<int:company_id>/images/
