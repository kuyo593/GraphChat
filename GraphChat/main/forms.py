from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

from django.contrib.auth.models import User
from .models import User
from django.core.exceptions import ValidationError
from django.core.validators import ( FileExtensionValidator)

class SignUpForm(UserCreationForm):
   img = forms.ImageField( required=False, validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],)
   class Meta:
    model = User
    fields = ('username', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    pass