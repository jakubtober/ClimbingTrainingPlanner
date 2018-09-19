from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_instructor = models.BooleanField(default=False)
    activation_token = models.CharField(max_length=64, default=uuid4())
