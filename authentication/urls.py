from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import SignupView, CustomLoginView


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='my_logout'),
    path('signup/', SignupView.as_view(), name='signup'),
]
