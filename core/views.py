from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .forms import CustomUserCreationForm


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')


class Login(FormView):
    template_name = 'core/login.html'
    form_class = AuthenticationForm
    success_url = '/'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        return redirect(self.get_success_url())


class Register(FormView):
    template_name = 'core/registration.html'
    form_class = CustomUserCreationForm
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())
