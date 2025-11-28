from django.contrib import admin
from .models import FriendPost, PostLike, PostComment

admin.site.register([FriendPost, PostLike, PostComment])
