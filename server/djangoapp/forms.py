from django import forms
from django.contrib.auth.models import User
# to create registration using django template
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    #email = forms.EmailField()

    class Meta:
        model = User
        #fields = ["username", "email", "password1", "password2"]
        fields = ["username", "first_name", "last_name", "password1", "password2"]
