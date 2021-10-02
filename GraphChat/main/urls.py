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
    path('my_page',views.my_page,name='my_page'),
    path ('topic/<int:id>',views.topic,name='topic'),
    

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)