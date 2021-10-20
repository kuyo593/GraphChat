from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.forms.fields import JSONField
from datetime import datetime
from django.contrib.postgres.fields import ArrayField
from django.db.models.fields.related import ManyToManyField



class User(User):
    #talk = JSONField()
    pass

#登録　user ( username=demii password=ty2345ty  username = ad paass = yu6789iu)

class UserImage(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_img")
   image = models.ImageField(verbose_name="画像", null=True, blank=True, upload_to="images")

class Talk(models.Model):
   talk = models.CharField(null=False,max_length=500)
   talk_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="talk_from",null=True) #topicを保存する時はnullで
   talk_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="talk_to",null=True)
   child_talk_id = ArrayField(models.IntegerField(), null=True, blank=True)
   time = models.DateTimeField(default=datetime.now)

class Topic(models.Model):
   user=ManyToManyField(User)
   
   topic = ArrayField(models.IntegerField(),null=False) #[talkモデルのidを保存]



class Group(models.Model):
   name=models.CharField(null=False,max_length=36)
   #topic=ArrayField()

class GroupImage(models.Model):
   user = models.OneToOneField(Group, on_delete=models.CASCADE, related_name="group_img")
   image = models.ImageField(verbose_name="画像", null=True, blank=True, upload_to="images")

