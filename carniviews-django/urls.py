from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('authentication_app.urls')),
    # path('', include('authentication_app.urls')),
    # path('', include('members_app.urls')),
    path('reviews/', include('review_app.urls')),
    path('bryan/', include('book_app.urls')), #bryan/books
    path('admin/', admin.site.urls),
]