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
    activation_token = models.CharField(max_length=128, default='')

    def send_activation_email(self):
        activation_message ="""
        Hi {},

        Welcome in weClimb, please click following link to activate your account:

        http://127.0.0.1:8000/register/activate?token={}

        Thank you,
        weClimb team
        """.format(self.user.username, self.activation_token)

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
        self.activation_token = ''
        self.save()
