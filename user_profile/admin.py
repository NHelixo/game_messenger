from django.contrib import admin

from .models import UserFriend, ChatMessage, UserPicture, Chat

admin.site.register([UserFriend, ChatMessage, UserPicture, Chat])
