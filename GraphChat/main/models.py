
from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.forms.fields import JSONField
from django.contrib.postgres.fields import ArrayField



class User(User):
    talk = JSONField()

#登録　user (username = demia password = hujyi4597  )

class UserImage(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_img")
   image = models.ImageField(verbose_name="画像", null=True, blank=True, upload_to="images")

class Talk(models.Model):
   talk = models.CharField(blank=True,max_length=500)
   talk_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="talk_from")
   time = models.DateTimeField(auto_now_add=True),
   child_talk_id=ArrayField(models.IntegerField(blank=True),null=True)

