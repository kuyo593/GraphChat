from django.contrib.postgres.fields import array
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, TopicForm, ProfileChangeForm, TalkForm, BranchForm, GroupCreationForm
from django.contrib.auth import authenticate, get_user, login
from django.contrib.auth.views import LoginView
from .models import Group, GroupImage, User, UserImage ,Talk ,Topic, Example
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
    all_group = Group.objects.all()
    if len(all_group) != 0:

        #あとで最新トークの時間に応じてソートする機能をつける
        no_topic_group = [] #[Group object, GroupImage object]
        before_sort_group = [] #[Group object, GroupImage object]

        for one_group in all_group:
            one_group_image = GroupImage.objects.get(group=one_group)
            if one_group.topic['id'] is not None:
                #各グループの最新トークの時間を取得
                one_group_topic_time = []

                for topic_id in one_group.topic['id']:
                    one_group_topic_time.append(Talk.objects.get(id=topic_id).time)
                new_time = max(one_group_topic_time)

                #メモ、image忘れてる、lambaつかってfriendの時と同じようにソート
                

                before_sort_group.append([one_group, one_group_image, new_time])

            else:
                no_topic_group.append([one_group, one_group_image])
        
        after_sort_group = sorted(before_sort_group, reverse=True, key=lambda x: x[2])
        sorted_all_group = after_sort_group + no_topic_group
        params = {
            'sorted_all_group': sorted_all_group
            }
        return render(request,'main/group.html', params)
    else:
        no_group_message = 'グループは存在していません。'
        params = {
            'no_group_message': no_group_message,
        }

        return render(request,'main/group.html', params)

@login_required
def group_creation(request):
    if request.method == 'GET':
        form = GroupCreationForm()
        params = {'form': form,}
        return render(request, 'main/group_creation.html', params)
    elif request.method == 'POST':
        form = GroupCreationForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            image = form.cleaned_data.get('image')

            new_group = Group(name=name)
            new_group.save()
            
            new_group_image = GroupImage(group=new_group, image=image)
            new_group_image.save()

            topic_form = TopicForm()
            group_id = new_group.id
            params = {
                'topic_form' : topic_form,
                'group_id' : group_id, 
            }
    
            return render(request,'main/group_topic.html', params)
        else:
            form = GroupCreationForm()
            params = {
                'form': form,
                }
            return render(request, 'main/group_creation.html', params)

@login_required
def group_topic(request, group_id):
    group = Group.objects.get(id=group_id)
    if request.method == 'GET':
        group_image = GroupImage.objects.get(group=group)
        form = TopicForm()
        if group.topic != {}:
            topic_id = group.topic['id']
            topic_record = Talk.objects.filter(id__in=topic_id).order_by('time').reverse()

            params = {
                'topic_form': form,
                'group_topic': topic_record,
                'group_id': group.id,
                'group_image': group_image,
            }
        else:

            params = {
                'topic_form': form,
                'group_id': group.id,
                'group_image': group_image,
            }


        return render(request, 'main/group_topic.html', params)

    elif request.method == 'POST':
        new_topic_name = request.POST['topic']
        new_topic_record = Talk(talk=new_topic_name, talk_from=User.objects.get(id=request.user.id))
        new_topic_record.save()

        talk_content = [new_topic_record]

        form = TalkForm()
        form_bran = BranchForm()

        if Group.objects.get(id=group_id).topic != {}:
            all_topic = Group.objects.get(id=group_id).topic['id']
            all_topic.append(new_topic_record.id)
            Group.objects.filter(id=group.id).update(topic={'id': all_topic})


        else:
            all_topic = [new_topic_record.id]
            Group.objects.filter(id=group.id).update(topic={'id': all_topic})

        params = {
            'group_id': group_id,
            'form': form,
            'form_bran': form_bran,
            'talk_content': talk_content,
            'topic_id': new_topic_record.id
        }
        return render(request, 'main/group_talk.html', params)



@login_required
def group_talk(request, topic_id, group_id):
    if request.method == "GET":
        talk = Talk.objects.get(id=topic_id)
        if talk.parent_talk_id is not None: 
            parent=Talk.objects.get(id=talk.parent_talk_id)
            out_count = 1
            while (out_count == 1) and parent.parent_talk_id is not None:
                pre_parent = parent
                parent=Talk.objects.get(id=parent.parent_talk_id)
                if len(parent.child_talk_id['id']) != 1:
                    out_count +=1
            if out_count == 2:
                return_id = pre_parent.id
            else:
                return_id = parent.id
            return_url_name = 'talk'
        else:
            return_id = group_id
            return_url_name = 'topic'

        talk_content = [talk]
        child_judge = talk.child_talk_id
        multiple_judge =0
        if child_judge != {}:
            multiple_judge= len(child_judge['id'])

        while child_judge != {} and multiple_judge < 2:
            child_talk = Talk.objects.get(id=talk_content[-1].child_talk_id['id'][0])
            talk_content.append(child_talk)
            child_judge = child_talk.child_talk_id
            if child_judge != {}:
                multiple_judge= len(child_judge['id'])

            

        branch_talk = []
        if multiple_judge >= 2:
            length = multiple_judge
            count = 0
            while count < length:
                branch_talk.append(Talk.objects.get(id=child_judge['id'][count]))
                count += 1
        form = TalkForm()
        form_bran = BranchForm()
        params = {
            'talk_content': talk_content,
            'form': form,
            'form_bran': form_bran,
            'branch_talk': branch_talk,
            'group_id': group_id,
            'topic_id': topic_id,
            'return_url_name': return_url_name,
            'return_id': return_id,
        }
        return render(request, 'main/group_talk.html', params)



    elif request.method == "POST":
        talk = Talk.objects.get(id=topic_id)
        
        if 'talk' in request.POST:#request.POST['talk']の時は新しくトークの枝を切っていない場合
            if talk.parent_talk_id is not None: 
                parent=Talk.objects.get(id=talk.parent_talk_id)
                out_count = 1
                while (out_count == 1) and parent.parent_talk_id is not None:
                    pre_parent = parent
                    parent=Talk.objects.get(id=parent.parent_talk_id)
                    if len(parent.child_talk_id['id']) != 1:
                        out_count +=1
                if out_count == 2:
                    return_id = pre_parent.id
                else:
                    return_id = parent.id
                 
                return_url_name = 'talk'
            else:
                 return_id = group_id
                 return_url_name = 'topic'

            child_judge = talk.child_talk_id
            #multiple_judge= talk.child_talk_id['id'].length() 必要なし
            talk_content = [talk]
            child_talk = talk
            while child_judge != {}:
                child_talk = Talk.objects.get(id=child_talk.child_talk_id['id'][0])
                talk_content.append(child_talk)
                child_judge = child_talk.child_talk_id
                #multiple_judge= child_talk.child_talk_id['id'].length() 必要なし

            talk = request.POST['talk']
            talk_save = Talk(talk=talk, talk_from=User.objects.get(id=request.user.id),  parent_talk_id=topic_id)
            talk_save.save()
            talk_content.append(talk_save)
            
            Talk.objects.filter(id=child_talk.id).update(child_talk_id={'id': [talk_save.id]})



            form = TalkForm()
            form_bran = BranchForm()
            params = {
                'talk_content': talk_content,
                'form': form,
                'form_bran': form_bran,
                'group_id': group_id,
                'topic_id': topic_id,
                'return_url_name': return_url_name,
                'return_id': return_id,
            }
            return render(request, 'main/group_talk.html', params)

        elif 'branch_talk' in request.POST:#request.POST['branch_talk']の時は新しくトークの枝を切っていない場合
            parent=Talk.objects.get(id=topic_id)
            out_count = 1
            while (out_count == 1) and parent.parent_talk_id is not None:
                pre_parent = parent
                parent=Talk.objects.get(id=parent.parent_talk_id)
                if len(parent.child_talk_id['id']) != 1:
                    out_count +=1
            if out_count == 2:
                return_id = pre_parent.id
            else:
                return_id = parent.id
            return_url_name = 'talk'

            branch_talk = request.POST['branch_talk']
            talk_save = Talk(talk=branch_talk, talk_from=User.objects.get(id=request.user.id), parent_talk_id=topic_id)
            talk_save.save()

            child_list = talk.child_talk_id['id']
            child_list.append(talk_save.id)
            Talk.objects.filter(id=topic_id).update(child_talk_id={'id': child_list})
            
            talk_content = [talk_save]
            form = TalkForm()
            
            params = {
                'talk_content': talk_content,
                'form': form,
                'group_id': group_id,
                'topic_id': talk_save.id,
                'return_url_name': return_url_name,
                'return_id': return_id,
            }
            return render(request, 'main/group_talk.html', params)





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
def topic(request, id):
    user_id = request.user.id
    if request.method == "GET":
        partnerUser = User.objects.get(id = id)
        myUser = User.objects.get(id = user_id)
        partner_image = UserImage.objects.get(user=partnerUser)
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
                params = {
                    'form' : form,
                    'partnerUser' : partnerUser,
                    'partner_image': partner_image,
                    'id': id,
                }
                return render(request,'main/topic.html',params)


        else:
            form = TopicForm()
            params = {
                'form' : form,
                'partnerUser' : partnerUser,
                'partner_image': partner_image,
                'id': id,
            }

            return render(request,'main/topic.html',params)

    elif request.method == "POST": #トピックを作るページ
        talk = request.POST['topic']
        topic = Talk(talk=talk, talk_from=User.objects.get(id=request.user.id))
        topic.save()
        topic_id=topic.id
        myUser = User.objects.get(id = user_id)
        partnerUser = User.objects.get(id = id)

        talk_content = [topic]

        form = TalkForm()
        form_bran = BranchForm()

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
                    'topic_id': topic_id,
                    'form': form,
                    'form_bran': form_bran,
                    'id': id,
                    'talk_content': talk_content,
                }
                return render(request, 'main/talk.html', params)

            else:
                talk_id = []
                talk_id.append(topic_id)
                topic_obj=Topic.objects.create(topic=dict(id=talk_id)) 
                topic_obj.user.add(myUser)
                topic_obj.user.add(partnerUser)

                params = {
                        'topic_id': topic_obj.id,
                        'form': form,
                        'form_bran': form_bran,
                        'id': id,
                        'talk_content': talk_content,
                    }
                return render(request, 'main/talk.html', params)                

        else:
            talk_id = []
            talk_id.append(topic_id)
            topic_obj=Topic.objects.create(topic=dict(id=talk_id)) 
            topic_obj.user.add(myUser)
            topic_obj.user.add(partnerUser)
            
            params = {
                    'topic_id': topic_obj.id,
                    'form': form,
                    'form_bran': form_bran,
                    'id': id,
                    'talk_content': talk_content,
                }
            return render(request, 'main/talk.html', params)
            
@login_required
def talk(request, topic_id, id):

    
    if request.method == "GET":
        talk = Talk.objects.get(id=topic_id)
        if talk.parent_talk_id is not None: 
            parent=Talk.objects.get(id=talk.parent_talk_id)
            out_count = 1
            while (out_count == 1) and parent.parent_talk_id is not None:
                pre_parent = parent
                parent=Talk.objects.get(id=parent.parent_talk_id)
                if len(parent.child_talk_id['id']) != 1:
                    out_count +=1
            if out_count == 2:
                    return_id = pre_parent.id
            else:
                return_id = parent.id
            return_url_name = 'talk'
        else:
            return_id = id
            return_url_name = 'topic'

        talk_content = [talk]
        child_judge = talk.child_talk_id
        multiple_judge =0
        if child_judge != {}:
            multiple_judge= len(child_judge['id'])

        while child_judge != {} and multiple_judge < 2:
            child_talk = Talk.objects.get(id=talk_content[-1].child_talk_id['id'][0])
            talk_content.append(child_talk)
            child_judge = child_talk.child_talk_id
            if child_judge != {}:
                multiple_judge= len(child_judge['id'])

            

        branch_talk = []
        if multiple_judge >= 2:
            length = multiple_judge
            count = 0
            while count < length:
                branch_talk.append(Talk.objects.get(id=child_judge['id'][count]))
                count += 1
        form = TalkForm()
        form_bran = BranchForm()
        params = {
            'talk_content': talk_content,
            'form': form,
            'form_bran': form_bran,
            'branch_talk': branch_talk,
            'id': id,
            'topic_id': topic_id,
            'return_url_name': return_url_name,
            'return_id': return_id,
        }
        return render(request, 'main/talk.html', params)



    elif request.method == "POST":
        talk = Talk.objects.get(id=topic_id)
        
        if 'talk' in request.POST:#request.POST['talk']の時は新しくトークの枝を切っていない場合
            if talk.parent_talk_id is not None: 
                parent=Talk.objects.get(id=talk.parent_talk_id)
                out_count = 1
                while (out_count == 1) and parent.parent_talk_id is not None:
                    pre_parent = parent
                    parent=Talk.objects.get(id=parent.parent_talk_id)
                    if len(parent.child_talk_id['id']) != 1:
                        out_count +=1
                if out_count == 2:
                    return_id = pre_parent.id
                else:
                    return_id = parent.id
                 
                return_url_name = 'talk'
            else:
                 return_id = id
                 return_url_name = 'topic'

            child_judge = talk.child_talk_id
            #multiple_judge= talk.child_talk_id['id'].length() 必要なし
            talk_content = [talk]
            child_talk = talk
            while child_judge != {}:
                child_talk = Talk.objects.get(id=child_talk.child_talk_id['id'][0])
                talk_content.append(child_talk)
                child_judge = child_talk.child_talk_id
                #multiple_judge= child_talk.child_talk_id['id'].length() 必要なし

            talk = request.POST['talk']
            talk_save = Talk(talk=talk, talk_from=User.objects.get(id=request.user.id),  parent_talk_id=topic_id)
            talk_save.save()
            talk_content.append(talk_save)
            
            Talk.objects.filter(id=child_talk.id).update(child_talk_id={'id': [talk_save.id]})



            form = TalkForm()
            form_bran = BranchForm()
            params = {
                'talk_content': talk_content,
                'form': form,
                'form_bran': form_bran,
                'id': id,
                'topic_id': topic_id,
                'return_url_name': return_url_name,
                'return_id': return_id,
            }
            return render(request, 'main/talk.html', params)

        elif 'branch_talk' in request.POST:#request.POST['branch_talk']の時は新しくトークの枝を切っていない場合
            parent=Talk.objects.get(id=topic_id)
            out_count = 1
            while (out_count == 1) and parent.parent_talk_id is not None:
                pre_parent = parent
                parent=Talk.objects.get(id=parent.parent_talk_id)
                if len(parent.child_talk_id['id']) != 1:
                    out_count +=1
            if out_count == 2:
                return_id = pre_parent.id
            else:
                return_id = parent.id
            return_url_name = 'talk'

            branch_talk = request.POST['branch_talk']
            talk_save = Talk(talk=branch_talk, talk_from=User.objects.get(id=request.user.id), parent_talk_id=topic_id)
            talk_save.save()

            child_list = talk.child_talk_id['id']
            child_list.append(talk_save.id)
            Talk.objects.filter(id=topic_id).update(child_talk_id={'id': child_list})
            
            talk_content = [talk_save]
            form = TalkForm()
            
            params = {
                'talk_content': talk_content,
                'form': form,
                'id': id,
                'topic_id': talk_save.id,
                'return_url_name': return_url_name,
                'return_id': return_id,
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
        else:
            form = ProfileChangeForm()
            params = {
                'form': form,
                }
        return render(request, 'main/my_page.html', params)

