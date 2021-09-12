
from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.forms.fields import JSONField


class User(User):
   pass

class AUser(AbstractUser):
    pass

#登録　user (username = demia password = hujyi4597 ,username = demi password = 456yui890 ,
# username = de password = jkjdfijej5 )

class UserImage(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_img")
   image = models.ImageField(verbose_name="画像", null=True, blank=True, upload_to="images")

