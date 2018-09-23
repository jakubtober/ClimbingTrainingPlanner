from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views import View
from planner_app.models import Profile
from django.http import HttpResponse
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
        enter_correct_credentials_message = 'Please enter correct credentials.'
        activate_account_message = 'Please activate your account first'
        try_later_message = 'Sorry, please try again later.'

        ctx = {
            'form': form,
        }

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_exists = User.objects.filter(username=username)

            if user_exists:
                if user_exists[0].is_active == True:
                    user = authenticate(username=username, password=password)
                    if user:
                        login(request, user)
                        return redirect('home')
                    else:
                        form.add_error(field=None, error=try_later_message)
                        return render(request, 'login.html', ctx)
                else:
                    form.add_error(field=None, error=activate_account_message)
                    return render(request, 'login.html', ctx)
            else:
                form.add_error(field=None, error=enter_correct_credentials_message)
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
        activation_message = 'We have sent email with activation link to your email box, please click it to activate your account.'
        password_validation_message = 'Password needs to have minimum 6 characters.'
        use_different_username_email_message = 'Please user different username and/or email.'
        enter_correct_credentials_message = 'Please enter correct details.'

        ctx = {
            'form': form,
        }

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            is_instructor = form.cleaned_data['is_instructor']

            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                form.add_error(field=None, error=use_different_username_email_message)
                return render(request, 'register.html', ctx)
            else:
                if len(password) < 6:
                    form.add_error(field=None, error=password_validation_message)
                    return render(request, 'register.html', ctx)
                else:
                    new_user = User.objects.create_user(
                        username=username,
                        email=email,
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
                        'please_activate_your_account_message': 'You should receive email with activation link, please use it to activate your account.'
                    }
                    return render(request, 'login.html', ctx)
        else:
            form.add_error(field=None, error=enter_correct_credentials_message)
            return render(request, 'register.html', ctx)
        return render(request, 'register.html', ctx)


class ActivateUserView(View):
    def get(self, request):
        token = request.GET['token']

        try:
            users_profile_with_token = Profile.objects.get(activation_token=token)
            user_with_token = users_profile_with_token.user

            if default_token_generator.check_token(user_with_token, token):
                user_with_token.is_active = True
                user_with_token.save()
                ctx = {
                    'form': LoginForm,
                    'activation_message_success': 'User successfully activated.'
                }
                return render(request, 'login.html', ctx)
            else:
                ctx = {
                    'form': LoginForm,
                    'activation_message_unsuccessful': "Couldn't activate account, token is not correct."
                }
                return render(request, 'login.html', ctx)
        except:
            ctx = {
                'form': LoginForm,
                'activation_message_unsuccessful': 'Account has been already activated or there is no such user anymore.'
            }
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
        return render(request, 'home.html')
