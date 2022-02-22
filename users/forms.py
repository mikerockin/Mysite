from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    birthdate = forms.DateField(label='Дата рождения', help_text='Например: 2006-10-25')
    instagram = forms.CharField(max_length=100)


    class Meta:
        model = User
        fields = ["username", "birthdate", "email", "instagram", "password1", "password2"]




