from django.urls import path
from .views import new_acceptance, search_acceptance_good, acceptance_detail


urlpatterns = [
    path('new_acceptance/', new_acceptance, name='new-acceptance'),
    path('search_acceptance_good/', search_acceptance_good, name='search-acceptance-good'),
    path('acceptance_detail/<int:pk>/', acceptance_detail, name='acceptance-detail'),
]