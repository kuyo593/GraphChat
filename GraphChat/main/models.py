from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.forms.fields import JSONField
#from django.contrib.postgres.fields import ArrayField



class User(User):
    talk = JSONField()

#登録　user (username = demia password = hujyi4597 username=demi password=ty2345ty )

class UserImage(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_img")
   image = models.ImageField(verbose_name="画像", null=True, blank=True, upload_to="images")

class Talk(models.Model):
   talk = models.CharField(null=False,max_length=500)
   talk_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="talk_from",null=False)
   talk_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="talk_to",null=False)
   time = models.DateTimeField(auto_now_add=True)
   child_talk_id=JSONField()

class Group(models.Model):
   name=models.CharField(null=False,max_length=36)
   topic=JSONField()

class GroupImage(models.Model):
   user = models.OneToOneField(Group, on_delete=models.CASCADE, related_name="group_img")
   image = models.ImageField(verbose_name="画像", null=True, blank=True, upload_to="images")

