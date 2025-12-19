from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, RedirectView, UpdateView
from django.views import View
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from user_profile.models import UserFriend
from .models import UserCommunity, CommunityMember, CommunityRole


class Community(DetailView):
    model = UserCommunity
    template_name = "community/community.html"
    context_object_name = "community"

    def get_object(self, queryset=None):
        # Отримуємо id з URL-шляхів через self.kwargs
        community_id = self.kwargs.get('id')
        # Повертаємо об'єкт або 404, якщо не знайдено
        return get_object_or_404(UserCommunity, id=community_id)

class AddRole(View):
    model = CommunityRole
    template_name = "community/add_role.html"
    context_object_name = "role"

    def post(self, id):
        pass