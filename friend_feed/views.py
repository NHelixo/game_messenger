from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, RedirectView
from .models import FriendPost, PostLike, PostComment
from user_profile.models import UserFriend
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse,  HttpResponseRedirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.urls import reverse


class PostFeed(ListView):
    model = FriendPost
    template_name = "friend_feed/post_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        user = self.request.user
        friends = UserFriend.objects.filter(user=user, status='accepted').values_list('friend', flat=True)
        friends_of_user = UserFriend.objects.filter(friend=user, status='accepted').values_list('user', flat=True)

        all_friends = list(friends) + list(friends_of_user) + [user.id]

        return FriendPost.objects.filter(user__in=all_friends).annotate(like_count=Count('postlike'))


@method_decorator(login_required, name='dispatch')
class ToggleLikeView(View):
    def post(self, request, post_id):
        post = FriendPost.objects.get(id=post_id)
        user = request.user

        existing_like = PostLike.objects.filter(post=post, user=user).first()

        if existing_like:
            existing_like.delete()
        else:
            PostLike.objects.create(post=post, user=user)

        return HttpResponseRedirect(reverse('friend_feed:post_feed'))
    

@method_decorator(login_required, name='dispatch')
class AddComment(View):
    def post(self, request, post_id):
        post = FriendPost.objects.get(id=post_id)
        user = request.user
        comment = request.POST.get("comment_text")

        PostComment.objects.create(post=post, user=user, text=comment)

        return HttpResponseRedirect(reverse('friend_feed:post_feed'))

