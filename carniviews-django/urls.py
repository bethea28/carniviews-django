from django.contrib import admin
from django.urls import include, path

# urlpatterns = [
#     path('', include('authentication_app.urls')),
#     # path('', include('authentication_app.urls')),
#     path('', include('members_app.urls')),
#     path('reviews/', include('review_app.urls')),
#     path('addCompany/', include('company_app.urls')),
#     path('addImages/', include('images_app.urls')),
#     path('companies/<int:company_id>/images/', include('images_app.urls')), #Correct url pattern.
#     path('bryan/', include('book_app.urls')), #bryan/books
#     path('admin/', admin.site.urls),
# ]

urlpatterns = [
    path('authentication/', include('authentication_app.urls')),
    path('reviews/', include('review_app.urls')),
    path('ratings/', include('rating_app.urls')),
    path('company/', include('company_app.urls')),  # Group under /companies/
    path('bryan/', include('book_app.urls')),
    path('admin/', admin.site.urls),
]