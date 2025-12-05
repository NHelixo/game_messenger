from django.contrib import admin

from .models import UserFriend, ChatMessage, UserPicture

admin.site.register([UserFriend, ChatMessage, UserPicture])
