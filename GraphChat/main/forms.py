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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder':'Name'})
        self.fields['password1'].widget.attrs.update({'placeholder':'Password'})        

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Name'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))

class TopicForm(forms.Form):
    topic = forms.CharField(label='topic', required=True)
    

class ProfileChangeForm(forms.Form):
    username = forms.CharField(label='username', required=False, widget=TextInput(attrs={'class':'validate','placeholder': 'Name'}))
    image = forms.ImageField(label='image', required=False)
    password = forms.CharField(label='password', required=False, widget=PasswordInput(attrs={'placeholder':'Password'}))