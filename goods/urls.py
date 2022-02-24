from django.urls import path
from .views import good_list, create_good, delete_good, edit_good, update_good, check_barcode


urlpatterns = [
    path('goods/', good_list, name='goods'),
    path('create_good/', create_good, name='create-good'),
    path('goods/check_barcode/', check_barcode, name='check-barcode'),
    path('delete_good/<int:pk>/', delete_good, name='delete-good'),
    path('edit_good/<int:pk>/', edit_good, name='edit-good'),
    path('update_good/<int:pk>/', update_good, name='update-good'),
]