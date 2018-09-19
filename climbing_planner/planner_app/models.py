from django.db import models
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail
from uuid import uuid4

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_instructor = models.BooleanField(default=False)
    activation_token = models.CharField(max_length=64, default=uuid4())

    def send_activation_email(self):
        activation_message ="""
        Hi {},

        Welcome in weClimb, please click following link to activate your account:

        http://127.0.0.1:8000/login/activate/{}

        Thank you,
        weClimb team
        """.format(self.user.username, self.activation_token)

        send_mail(
            'Activate account - weClimb',
            activation_message,
            'climbing.planner@gmail.com',
            [str(self.user.email)],
            fail_silently=False,
        )
