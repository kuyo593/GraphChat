from django.shortcuts import render, redirect
from .forms import SignUpForm,LoginForm
from django.contrib.auth import authenticate, get_user, login
from django.contrib.auth.views import LoginView
from .models import User, UserImage
from django.contrib.auth.decorators import login_required
import logging


# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def signup(request):
    
    if request.method == "GET":
        form = SignUpForm()
        params = {"form": form, }
        return render(request, "main/signup.html", params)
    elif request.method == "POST":
        
        form = SignUpForm(request.POST, request.FILES)
        logging.debug(form.errors)
        if form.is_valid():
            
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            image = form.cleaned_data.get('img')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                logging.debug('yy')
                
                login(request, user)
                user = User.objects.get(username=username)
                user_img = UserImage(user=user,image=image,)             
                user_img.save()
        params = {"form": form, }
        logging.debug('yyy')
        return render(request, "main/signup.html", params)


class Login(LoginView):
    authentication_form = LoginForm
    template_name = 'main/login.html'


@login_required
def home(request):
    user = request.user
    params={"user": user,}
    return render(request, 'main/home.html',params)

@login_required
def group(request):
    return render(request,'main/group.html')

@login_required
def friends(request):
    return render(request,'main/friends.html')

@login_required
def my_page(request):
    return render(request,'main/my_page.html')


