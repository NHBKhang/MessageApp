from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.models import PublicKey
from django import forms


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class PublicKeyForm(forms.ModelForm):
    class Meta:
        model = PublicKey
        fields = ['key', 'user']
