from django.contrib import admin
from .models import User,UserImage,Talk,Group,GroupImage,Topic
admin.site.register(User)
admin.site.register(UserImage)
admin.site.register(Talk)
admin.site.register(Group)
admin.site.register(GroupImage)
admin.site.register(Topic)


# Register your models here.

#superuser登録 usernmame= admin email= g70579@icloud.com pass= ki5688gh