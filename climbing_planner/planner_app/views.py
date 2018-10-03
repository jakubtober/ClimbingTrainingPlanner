from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views import View
from django.http import HttpResponse
from planner_app import custom_messages
from planner_app.models import Profile
from planner_app.forms import (
    LoginForm,
    RegisterForm,
    ResetPasswordForm,
)

# Create your views here.

class WelcomeView(View):
    def get(self, request):
        return render(request, 'welcome.html')


class LoginView(View):
    def get(self, request):
        ctx = {
            'form': LoginForm,
        }
        return render(request, 'login.html', ctx)

    def post(self, request):
        form = LoginForm(request.POST)

        ctx = {
            'form': form,
        }

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(field=None, error=custom_messages.enter_correct_credentials)
        return render(request, 'login.html', ctx)


class LogoutView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        logout(request)
        return redirect('login')


class RegisterView(View):
    def get(self, request):
        ctx = {
            'form': RegisterForm,
        }
        return render(request, 'register.html', ctx)

    def post(self, request):
        form = RegisterForm(request.POST)

        ctx = {
            'form': form,
        }

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            is_instructor = form.cleaned_data['is_instructor']

            new_user = User.objects.create_user(
                username=username,
                password=password,
                is_active=False
            )
            new_profile = Profile.objects.create(
                user=new_user,
                is_instructor=is_instructor,
                activation_token=default_token_generator.make_token(new_user)
            )
            new_profile.send_activation_email()
            ctx = {
                'form': LoginForm,
                'please_activate_your_account_message': custom_messages.activation_email_sent,
            }
            return render(request, 'login.html', ctx)
        else:
            return render(request, 'register.html', ctx)


class ActivateUserView(View):
    def get(self, request):
        token = request.GET['token']
        ctx = {
            'form': LoginForm,
        }

        try:
            users_profile_with_token = Profile.objects.get(activation_token=token)
            user_with_token = users_profile_with_token.user

            if default_token_generator.check_token(user_with_token, token):
                users_profile_with_token.activate_user()
                ctx['activation_message_success'] = custom_messages.user_successfully_activated
                return render(request, 'login.html', ctx)
            else:
                ctx['activation_message_unsuccessful'] = custom_messages.token_not_correct
                return render(request, 'login.html', ctx)
        except:
            ctx['activation_message_unsuccessful'] = custom_messages.account_already_activated
            return render(request, 'login.html', ctx)


class ResetPasswordView(View):
    def get(self, request):
        ctx = {
            'form': ResetPasswordForm,
        }
        return render(request, 'reset-password.html', ctx)


class HomeView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=request.user)
        ctx = {
            'profile': profile,
        }

        return render(request, 'home.html', ctx)
