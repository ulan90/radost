from django.urls import path
from .views import sale, search_good


urlpatterns = [
    path('', sale, name='sale'),
    path('search_good/', search_good, name='search'),
]