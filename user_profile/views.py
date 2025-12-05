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
from user_profile.models import UserFriend

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

        return redirect('core:login')
    

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

        print(f"Знайдено користувачів: {friends_users.count()}")

        return friends_users


class AcceptFriend(View):
    pass


class RejectFriend(View):
    pass
