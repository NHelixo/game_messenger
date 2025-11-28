from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, RedirectView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

class Profile(DetailView):
    model = User
    template_name = "user_profile/profile.html"
    context_object_name = "users"

    def get_object(self, queryset=None):
        user = get_object_or_404(User, id=self.request.user.id)
        return user


