from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms

class RegisterForm(UserCreationForm):
    # custom form register à partir de UserCreationForm
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", ]