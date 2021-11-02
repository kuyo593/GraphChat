from django.contrib.postgres.fields import array
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, TopicForm, ProfileChangeForm
from django.contrib.auth import authenticate, get_user, login
from django.contrib.auth.views import LoginView
from .models import User, UserImage ,Talk ,Topic, Example
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
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            image = form.cleaned_data.get('img')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                #login(request, user)でエラーがでたのでとりあえず別手段でログイン
                user = User.objects.get(username=username)
                user_img = UserImage(user=user,image=image,)             
                user_img.save()
                params={'user':user}
                return render(request,"main/home.html",params)
        params = {"form": form, }
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
            friendsTimeSort.append([friend,image[0],timeData['time__max']])
    friendsTimeSort = sorted(friendsTimeSort, reverse=True, key=lambda x: x[2])
    friendsTimeSort += friendsTime0
    params={"friends": friendsTimeSort, }
    return render(request,'main/friends.html',params)

@login_required
def topic(request,id):
    user_id = request.user.id
    if request.method == "GET":
        partnerUser = User.objects.get(id = id)
        myUser = User.objects.get(id = user_id)
        partner_image = UserImage.objects.filter(user=partnerUser)
        partner_image = partner_image[0]
        if Topic.objects.filter(user=id).count() != 0:
            my_partner_topic = Topic.objects.filter(user=id)
            if my_partner_topic.filter(user=user_id).count() != 0:
                my_partner_topic = my_partner_topic.get(user=user_id)
                my_partner_topic = my_partner_topic.topic['id']

                my_partner_topic_talk_record = Talk.objects.filter(id__in=my_partner_topic).order_by('time').reverse()
                form = TopicForm()

                params = {
                    'form': form,
                    'partnerUser' : partnerUser,
                    'partner_image': partner_image,
                    'id': id,
                    'topic': my_partner_topic_talk_record,      
                }

                return render(request,'main/topic.html',params)

        else:
            form = TopicForm()
        
        #あとでmyUser.talkの中に対象の人のトピックが一つでもあるか評価するようなコードｗを書く
        #userを作った時にmyUser.talkにusetr情報（情報はない）を追加するのもあり
        
            params = {
                'form' : form,
                'partnerUser' : partnerUser,
                'partner_image': partner_image,
                'id': id,
            }

            return render(request,'main/topic.html',params)

    elif request.method == "POST": #トピックを作るページ
        talk = request.POST['topic']
        topic = Talk(talk=talk)
        topic.save()
        topic_id=topic.id
        myUser = User.objects.get(id = user_id)
        partnerUser = User.objects.get(id = id)
        if Topic.objects.filter(user=id).count() != 0: #errorでたらフィルターは一つだけにしてもう一つはforループでなんとか　
            topic_filter_partner = Topic.objects.filter(user=id)
            if topic_filter_partner.filter(user=user_id).count() != 0:
                topic_obj = topic_filter_partner.get(user=user_id)
                talk_id_dict = topic_obj.topic
                talk_id = talk_id_dict['id']
                talk_id.append(topic_id)
                talk_id_dict = {'id': talk_id}
                topic_filter_partner.filter(user=user_id).update(topic=talk_id_dict)
                
                params = {
                    'topic': topic,
                }
                return render(request, 'main/talk.html', params)
                

        else:
            talk_id = []
            talk_id.append(topic_id)
            topic_obj=Topic.objects.create(topic=dict(id=talk_id)) 
            topic_obj.user.add(myUser)
            topic_obj.user.add(partnerUser)
            
            params = {
                    'topic': topic,
                }
            return render(request, 'main/talk.html', params)
            

@login_required
def my_page(request):
    if request.method == "GET":
        form = ProfileChangeForm()
        params = {
            'form': form,
        }
        return render(request, 'main/my_page.html', params)
        
    elif request.method == "POST":
        form = ProfileChangeForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            image = form.cleaned_data.get('image')
            user_id = request.user.id
            user = User.objects.get(id=user_id)
            if username != '':
                User.objects.filter(id=user_id).update(username=username)
            if password != '':
                User.objects.filter(id=user_id).update(password=password)
            if image != None:
                UserImage.objects.filter(user=user).update(image=image)
            return render(request,'main/home.html')

