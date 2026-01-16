from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, RedirectView, UpdateView
from django.views import View
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from .forms import ProfileEditForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from user_profile.models import UserFriend, Chat, ChatMessage
from community.models import UserCommunity, CommunityMember
from django.http import JsonResponse

class Profile(DetailView):
    model = User
    template_name = "user_profile/profile.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        user = get_object_or_404(User, id=self.request.user.id)
        return user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        pending_requests = UserFriend.objects.filter(friend=user, status="pending")
        senders = User.objects.filter(id__in=pending_requests.values('user'))

        context['senders'] = senders
        return context


class ProfileEdit(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'user_profile/edit_profile.html'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        old_password = form.cleaned_data.get('old_password')
        if not self.request.user.check_password(old_password):
            form.add_error('old_password', 'Невірний старий пароль')
            return self.form_invalid(form)

        form.save()

        user = self.request.user

        return redirect('user_profile:profile', pk=user.id)
    

class FriendList(ListView):
    model = UserFriend
    template_name = "user_profile/friends.html"
    context_object_name = "friends_users"
    
    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return []

        friends = UserFriend.objects.filter(user=user, status='accepted').values_list('friend', flat=True)
        friends_of_user = UserFriend.objects.filter(friend=user, status='accepted').values_list('user', flat=True)

        friends = list(friends) + list(friends_of_user)

        friends_users = User.objects.filter(id__in=friends)

        return friends_users


class AcceptFriend(View):
    def post(self, request, pk):
        user = request.user
        friend = get_object_or_404(User, id=pk)

        friendship = UserFriend.get_friendship(user, friend)

        if friendship:
            if friendship.status == "pending":
                friendship.status = "accepted"
                friendship.save()
                return redirect("user_profile:profile", pk=user.id)
            else:
                print("Щось пішло не так")
                return redirect("user_profile:profile", pk=user.id)
        else:
            print("Відносини між користувачами не знайдено.")
            return redirect("user_profile:profile", pk=user.id)



class RejectFriend(View):
    def post(self, request, pk):
        user = request.user
        friend = get_object_or_404(User, id=pk)

        friendship = UserFriend.get_friendship(user, friend)

        print(friendship.status)

        if friendship and friendship.status == "pending":
            friendship.delete()
            return redirect("user_profile:profile", pk=user.id)
        
        elif friendship and friendship.status == "accepted" or friendship and friendship.status == "blocked":
            friendship.delete()
            return redirect("user_profile:friends", pk=user.id)

        else:
            print("Відносини між користувачами не знайдено.")
            return redirect("user_profile:profile", pk=user.id)


class Communities(ListView):
    model = UserCommunity
    template_name = "user_profile/communities.html"
    context_object_name = "communities"

    def get_queryset(self):
        user = self.request.user
        return UserCommunity.objects.filter(communitymember__user=user)


class ChatDetailView(DetailView):
    model = Chat
    template_name = 'user_profile/chat_detail.html'
    context_object_name = 'chat'

    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user).select_related('receiver')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chat = self.get_object()
        context['messages'] = ChatMessage.objects.filter(chat=chat).order_by('create_time')
        return context


class ChatCreateView(View):
    def post(self, request, *args, **kwargs):
        receiver_id = request.POST.get('receiver_id')
        receiver = get_object_or_404(User, id=receiver_id)

        chat = Chat.objects.filter(user=request.user, receiver=receiver) | Chat.objects.filter(user=receiver, receiver=request.user)
        
        if chat.exists():
            return JsonResponse({"message": "Chat already exists", "chat_id": chat.first().id})

        chat = Chat.objects.create(user=request.user, receiver=receiver)
        return JsonResponse({"message": "Chat created", "chat_id": chat.id})
    

class ChatMessageCreateView(View):
    def post(self, request, *args, **kwargs):
        chat_id = request.POST.get('chat_id')
        text = request.POST.get('text')

        chat = get_object_or_404(Chat, id=chat_id)

        message = ChatMessage.objects.create(
            chat=chat,
            user=request.user,
            text=text
        )

        return JsonResponse({
            "message": "Message sent",
            "message_id": message.id,
            "text": message.text,
            "create_time": message.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        })


class AddRole(View):
    pass
