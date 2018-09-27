from django.test import TestCase
from planner_app.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from planner_app.forms import (
    LoginForm,
    RegisterForm,
    ResetPasswordForm,
)

class ValidatePassword(TestCase):
    def setUp(self):
        password1 = 'test2018'
        password2 = 'test2018a'

        active_user = User.objects.create_user(
            username='test1',
            password=password1,
            is_active=True
        )
        inactive_user = User.objects.create_user(
            username='usernam2',
            password=password2,
            is_active=False
        )
        instructor_user_profile = Profile.objects.create(
            user=active_user,
            is_instructor=True,
            activation_token=default_token_generator.make_token(active_user)
        )
        none_instructor_user_profile = Profile.objects.create(
            user=inactive_user,
            is_instructor=False,
            activation_token=default_token_generator.make_token(inactive_user)
        )

    def test_user_creation(self):
        active_user = User.objects.get(username='test1')
        
        self.assertEqual(active_user.username, 'test1')
        self.assertEqual(active_user.is_active, True)
