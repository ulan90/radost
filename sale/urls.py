from django.urls import path
from .views import sale


urlpatterns = [
    path('sale/', sale, name='sale'),
]