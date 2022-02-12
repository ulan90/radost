from django.urls import path
from .views import good_list, create_good, delete_good, update_good


urlpatterns = [
    path('goods/', good_list, name='goods'),
    path('create_good/', create_good, name='create-good'),
    path('delete_good/<int:pk>/', delete_good, name='delete-good'),
    path('update_good/<int:pk>/', update_good, name='update-good'),
]