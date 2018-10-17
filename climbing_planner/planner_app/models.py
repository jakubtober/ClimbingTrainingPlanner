from django.db import models
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth.tokens import default_token_generator
from planner_app import custom_messages
from uuid import uuid4

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_instructor = models.BooleanField(default=False)
    auth_token = models.CharField(max_length=128, default='', blank=True)

    def __str__(self):
        return self.user.username

    def generate_auth_token(self):
        self.auth_token = default_token_generator.make_token(self.user)
        self.save()

    def check_token(self, token):
        return default_token_generator.check_token(self.user, token)

    def send_activation_email(self):
        self.generate_auth_token()
        activation_message ="""
        Hi {},

        Welcome in weClimb, please click following link to activate your account:

        http://127.0.0.1:8000/register/activate?token={}

        Thank you,
        weClimb team
        """.format(self.user.username, self.auth_token)

        return send_mail(
            'Activate account - weClimb',
            activation_message,
            'climbing.planner@gmail.com',
            [str(self.user.username)],
            fail_silently=False,
        )

    def activate_user(self):
        self.user.is_active = True
        self.user.save()
        self.auth_token = ''
        self.save()

    def send_reset_password_email(self):
        self.generate_auth_token()
        activation_message ="""
        Hi {},

        Please click following link to change your password:

        http://127.0.0.1:8000/set-new-password?token={}

        Thank you,
        weClimb team
        """.format(self.user.username, self.auth_token)

        return send_mail(
            'Reset password - weClimb',
            activation_message,
            'climbing.planner@gmail.com',
            [str(self.user.username)],
            fail_silently=False,
        )

    def clear_auth_token(self):
        self.auth_token = ''
        self.save()
