from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.forms import AuthenticationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': ('Пароли не совпадают'),
    }

    class Meta:
        model = User
        fields = ('username',)
        field_classes = {'username': UsernameField}

class CustomLoginViewForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        'autofocus': True,
        'id': 'login',
        'class': 'fadeIn second',
        'name': 'login',
        'placeholder': 'Имя пользователя',
    }))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'id': 'password',
            'class': 'fadeIn third',
            'name': 'login',
            'placeholder': 'Пароль',
        }),
    )