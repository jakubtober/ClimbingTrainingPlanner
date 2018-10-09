from django import forms
from planner_app import custom_messages
from django.contrib.auth.models import User
from django.core.validators import validate_email

class LoginForm(forms.Form):
    username = forms.EmailField()
    password = forms.CharField(max_length=64, widget=forms.PasswordInput, label="")

    username.widget.attrs.update({
        'placeholder': 'email',
        'class':'validate',
        'data-length': '64',
        'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$',
    })
    password.widget.attrs.update({
        'placeholder': 'password',
        'class': 'validate',
    })

    def clean(self):
        data = self.cleaned_data
        try:
            username = data['username']
            if User.objects.filter(username=data['username']).exists():
                user = User.objects.get(username=data['username'])
                if not user.is_active:
                    self.add_error(field=None, error=custom_messages.activate_account)
            else:
                self.add_error(field=None, error=custom_messages.enter_correct_credentials)
        except KeyError:
            self.add_error(field=None, error=custom_messages.email_format_not_correct)


class RegisterForm(forms.Form):
    username = forms.EmailField()
    password = forms.CharField(max_length=64, widget=forms.PasswordInput, label="")
    confirm_password = forms.CharField(max_length=64, widget=forms.PasswordInput, label="")
    is_instructor = forms.BooleanField(required=False)

    username.widget.attrs.update({
        'placeholder': 'email',
        'class':'validate',
        'data-length': '64',
        'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$',
    })
    password.widget.attrs.update({
        'placeholder': 'password',
        'class': 'validate',
    })
    confirm_password.widget.attrs.update({
        'placeholder': 'confirm password',
        'class': 'validate',
    })

    def clean(self):
        data = self.cleaned_data
        try:
            username = data['username']
            if User.objects.filter(username=data['username']).exists():
                self.add_error(field=None, error=custom_messages.use_different_email)
            if len(data['password']) < 6:
                self.add_error(field=None, error=custom_messages.password_min_six_chars)
            if data['password'] != data['confirm_password']:
                self.add_error(field=None, error=custom_messages.passwords_not_matched)
        except KeyError:
            self.add_error(field=None, error=custom_messages.email_format_not_correct)


class ResetPasswordForm(forms.Form):
    email = forms.EmailField()

    email.widget.attrs.update({
        'placeholder': 'email',
        'class':'validate',
        'data-length': '64',
        'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$',
    })

    def clean(self):
        data = self.cleaned_data
        try:
            email = data['email']
            if not User.objects.filter(username=data['email']).exists():
                self.add_error(field=None, error=custom_messages.user_not_found)
        except KeyError:
            self.add_error(field=None, error=custom_messages.email_format_not_correct)


class SetNewPasswordForm(forms.Form):
    password = forms.CharField(max_length=64, widget=forms.PasswordInput, label="")
    confirm_password = forms.CharField(max_length=64, widget=forms.PasswordInput, label="")

    password.widget.attrs.update({
        'placeholder': 'new password',
        'class': 'validate',
    })

    confirm_password.widget.attrs.update({
        'placeholder': 'confirm password',
        'class': 'validate',
    })

    def clean(self):
        data = self.cleaned_data
        if len(data['password']) < 6:
            self.add_error(field=None, error=custom_messages.password_min_six_chars)
        if data['password'] != data['confirm_password']:
            self.add_error(field=None, error=custom_messages.passwords_not_matched)
