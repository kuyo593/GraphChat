from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import User,Talk,UserImage
from django.core.exceptions import ValidationError
from django.core.validators import ( FileExtensionValidator)

class SignUpForm(UserCreationForm):
   img = forms.ImageField( required=False, validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],)
   class Meta:
    model = User
    fields = ('username', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    pass

class TopicForm(ModelForm):
    class Meta:
        model = Talk
        fields = [
            'talk', 'time',
        ]

class ProfileChangeForm(forms.Form):
    username = forms.CharField(label='username', required=False)
    image = forms.ImageField(label='image', required=False)
    password = forms.CharField(label='password', required=False)