from django.shortcuts import reverse
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomLoginViewForm

# Create your views here.
class SignupView(CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse('login')


class CustomLoginView(LoginView):
    form_class = CustomLoginViewForm