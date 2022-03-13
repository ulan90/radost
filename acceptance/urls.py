from django.urls import path
from .views import new_acceptance


urlpatterns = [
    path('new_acceptance/', new_acceptance, name='new-acceptance'),
]