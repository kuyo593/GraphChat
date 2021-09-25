
from django.shortcuts import render, redirect
from .forms import SignUpForm,LoginForm
from django.contrib.auth import authenticate, get_user, login
from django.contrib.auth.views import LoginView
from .models import User, UserImage,Talk
from django.contrib.auth.decorators import login_required
import logging
import datetime
from django.db.models import Q,Max

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
                
                #login(request, user)
                user = User.objects.get(username=username)
                user_img = UserImage(user=user,image=image,)             
                user_img.save()
                params={'user':user}
                if image is None:
                    logging.debug('yyly')
                return render(request,"main/home.html",params)
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
    user = request.user
    friends = User.objects.exclude(id=user.id)
    friendsTimeSort=[] #ここのコードはもっと効率よくできるかもしれない
    friendsTime0=[]

    for friend in friends:
        timeData=Talk.objects.filter(Q(talk_from=user,talk_to=friend)|Q(talk_from=friend,talk_to=user)).aggregate(Max('time'))
        image = UserImage.objects.filter(user=friend)
    
        if timeData['time__max'] == None:
            friendsTime0.append([friend,image[0]])
        else:
            friendsTimeSort.append([friend,image,timeData['time__max']])
    friendsTimeSort = sorted(friendsTimeSort, reverse=True, key=lambda x: x[2])
    friendsTimeSort += friendsTime0
    

    
    params={"friends": friendsTimeSort, }
    return render(request,'main/friends.html',params)

@login_required
def topic(request,id):
    user = request.user.id
    if request.method == "GET":
        partnerUser = User.objects.get(id = id)
        myUser = User.objects.get(id = user)
        topic = myUser.talk

        params = {
            'topic': topic,

        }

        return render(request,'main/topic.html',params)

    elif request.method == "POST": #トピックを作るページ
        return render(request,'main/talk.html')


   

@login_required
def my_page(request):
    return render(request,'main/my_page.html')

