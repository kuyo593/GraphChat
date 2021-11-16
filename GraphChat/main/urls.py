from django.urls import path
from . import views
from .views import Login
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index, name='index'),
    path('signup',views.signup, name='signup'),
    path('login',Login.as_view(),name='login'),
    path('home',views.home,name='home'),
    path('friends',views.friends,name='friends'),
    path('group',views.group,name='group'),
    path('group_creation',views.group_creation,name='group_creation'),
    path('group_topic/<int:group_id>', views.group_topic, name='group_topic'),
    path('group_talk/<int:topic_id>/<int:group_id>', views.group_talk, name='group_talk'),
    path('my_page',views.my_page,name='my_page'),
    path('topic/<int:id>',views.topic,name='topic'),
    path('talk/<int:topic_id>/<int:id>', views.talk, name='talk'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)