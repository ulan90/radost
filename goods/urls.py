from django.urls import path
from .views import GoodListView


urlpatterns = [
    path('', GoodListView.as_view(), name='goods'),
]