from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.core.mail import send_mail
from django.urls import reverse_lazy

from utils import site_messages
from accounts.models import User
from . import forms


class Register(View):
    template_name = 'registration/register.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.context = {
            'register_form': forms.UserRegisterForm(self.request.POST or None),
        }
        self.register_form = self.context['register_form']

        self.render = render(self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.error(self.request,
                           site_messages.error['already_logged'])
            return redirect('posts:index')

        return self.render

    def post(self, *args, **kwargs):
        if not self.register_form.is_valid():
            return render(self.request, self.template_name, self.context)

        password = self.request.POST.get('password')

        user = self.register_form.save(commit=False)
        user.set_password(password)
        user.save()

        messages.success(
            self.request,
            site_messages.success['account_created']
        )
        return redirect('accounts:login')


class Login(View):
    template_name = 'registration/login.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.context = {
            'login_form': forms.UserLoginForm(self.request.POST or None),
        }
        self.login_form = self.context['login_form']

        self.render = render(self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.error(self.request,
                           site_messages.error['already_logged'])
            return redirect('posts:index')

        return self.render

    def post(self, *args, **kwargs):
        if not self.login_form.is_valid():
            return self.render

        email = self.request.POST.get('email')
        password = self.request.POST.get('password')

        auth = authenticate(self.request,
                            email=email,
                            password=password)

        if not auth:
            messages.error(self.request,
                           site_messages.error['login_incorrect_credentials'])
            return render(self.request, self.template_name, self.context)

        login(self.request, auth)

        messages.success(self.request,
                         site_messages.success['sucessfully_logged'])
        return redirect('posts:index')


def log_out(request):
    logout(request)

    messages.success(request,
                     site_messages.success['successfully_disconnected'])
    return redirect('accounts:login')
