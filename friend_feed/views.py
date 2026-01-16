from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, RedirectView
from .models import FriendPost, PostLike, PostComment
from community.models import UserCommunity
from user_profile.models import UserFriend
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse,  HttpResponseRedirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.urls import reverse
from django.shortcuts import render, redirect
from django.db.models import Q
from community.models import UserCommunity, CommunityMember


class PostFeed(ListView):
    model = FriendPost
    template_name = "friend_feed/post_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return []

        friends = UserFriend.objects.filter(user=user, status='accepted').values_list('friend', flat=True)
        friends_of_user = UserFriend.objects.filter(friend=user, status='accepted').values_list('user', flat=True)

        all_friends = list(friends) + list(friends_of_user) + [user.id]

        return FriendPost.objects.filter(user__in=all_friends).annotate(like_count=Count('postlike'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


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


class SearchFriend(ListView):
    model = User
    template_name = "friend_feed/search_friend.html"
    context_object_name = "friends"

    def get_queryset(self):
        user = self.request.user

        query = self.request.GET.get('q', '')

        friends = UserFriend.objects.filter(user=user).values_list('friend', flat=True)
        friends_of_user = UserFriend.objects.filter(friend=user).values_list('user', flat=True)
        friends = list(friends) + list(friends_of_user)

        all_users = User.objects.exclude(id=user.id).exclude(id__in=friends)

        if query:
            all_users = all_users.filter(username__icontains=query)

        return all_users


class SearchCommunity(ListView):
    model = UserCommunity
    template_name = "friend_feed/search_community.html"
    context_object_name = "community_list"

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        queryset = UserCommunity.objects.all()

        if query:
            queryset = queryset.filter(name__icontains=query) | queryset.filter(description__icontains=query)
        
        return queryset
    
    def post(self, request, *args, **kwargs):
        community_id = request.POST.get("community_id")
        user = request.user

        try:
            community = UserCommunity.objects.get(id=community_id)
        except UserCommunity.DoesNotExist:
            return redirect("friend_feed:search_community")

        if not CommunityMember.objects.filter(user=user, community=community).exists():
            CommunityMember.objects.create(user=user, community=community)

        return redirect("friend_feed:search_community")

class FriendRequest(View):                                                                                                                  
    def post(self, request, friend):
        user = request.user
        friend = get_object_or_404(User, id=friend)

        friend_request = UserFriend(user=user, friend=friend)
        friend_request.save()
        return redirect("friend_feed:search_friend")
