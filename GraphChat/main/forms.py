from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput
from .models import User, Talk, UserImage, Topic
from django.core.exceptions import ValidationError
from django.core.validators import ( FileExtensionValidator)

class SignUpForm(UserCreationForm):
   img = forms.ImageField( required=False, validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],)
   class Meta:
    model = User
    fields = ('username', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Name'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))

class TopicForm(forms.Form):
    topic = forms.CharField(label='topic', required=True)
    

class ProfileChangeForm(forms.Form):
    username = forms.CharField(label='username', required=False)
    image = forms.ImageField(label='image', required=False)
    password = forms.CharField(label='password', required=False)