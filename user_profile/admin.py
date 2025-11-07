from django.contrib import admin

from .models import UserFriend, ChatMessage

admin.site.register([UserFriend, ChatMessage])
