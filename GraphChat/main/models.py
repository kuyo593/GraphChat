from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.forms.fields import JSONField
from datetime import datetime
from django.contrib.postgres.fields import ArrayField
from django.db.models.fields.related import ManyToManyField

#!!!!!!!不必要なコメントはwebプリ完成後に一気に消します


class User(User):
    pass

#登録　user ( username=demii password=ty2345ty  username = ad paass = yu6789iu)

class UserImage(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_img")
   image = models.ImageField(verbose_name="画像", null=True, blank=True, upload_to="images")

class Talk(models.Model):
   talk = models.CharField(null=False,max_length=500)
   talk_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="talk_from",null=True) #topicを保存する時はnullで
   talk_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="talk_to",null=True)
   child_talk_id = JSONField() #Arrayfieldだと「unrecognized token: ":"」とエラーがでる
   time = models.DateTimeField(default=datetime.now)



class Topic(models.Model): #さしあたりトピック名が被るのを許す場合で作っていル
   user=ManyToManyField(User) #関係している人物全員選択（1体１のトークであれば、自分と相手、グループであればグループ内全員）
   #topic = ArrayField(models.IntegerField(),null=True) #[talkモデルのid(各トピックの最初の内容)を保存] 
   #最悪文字列をchairfieldで保存スル
   topic = models.JSONField(default=dict())

class Group(models.Model):
   name=models.CharField(null=False,max_length=36)

class GroupImage(models.Model):
   user = models.OneToOneField(Group, on_delete=models.CASCADE, related_name="group_img")
   image = models.ImageField(verbose_name="画像", null=True, blank=True, upload_to="images")


class Example(models.Model):
   array=ArrayField(models.IntegerField())