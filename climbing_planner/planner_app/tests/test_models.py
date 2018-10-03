from django.test import TestCase
from planner_app.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from planner_app.forms import (
    LoginForm,
    RegisterForm,
    ResetPasswordForm,
)

class ModelTest(TestCase):
    def setUp(self):
        active_user_name = 'test1@test.com'
        inactive_user_name = 'test2@test.com'
        active_user_password = 'test2018'
        inactive_user_password = 'test2018a'

        self.active_user = User.objects.create_user(
            username=active_user_name,
            password=active_user_password,
            is_active=True
        )
        self.inactive_user = User.objects.create_user(
            username=inactive_user_name,
            password=inactive_user_password,
            is_active=False
        )
        self.instructor_user_profile = Profile.objects.create(
            user=self.active_user,
            is_instructor=True,
            activation_token=default_token_generator.make_token(self.active_user)
        )
        self.none_instructor_user_profile = Profile.objects.create(
            user=self.inactive_user,
            is_instructor=False,
            activation_token=default_token_generator.make_token(self.inactive_user)
        )

    def test_user_creation(self):
        self.assertEqual(self.active_user.username, 'test1@test.com')
        self.assertEqual(self.active_user.is_active, True)

        self.assertEqual(self.inactive_user.username, 'test2@test.com')
        self.assertEqual(self.inactive_user.is_active, False)

        self.assertEqual(self.instructor_user_profile.user, self.active_user)
        self.assertEqual(self.none_instructor_user_profile.user, self.inactive_user)

        self.assertEqual(self.instructor_user_profile.is_instructor, True)
        self.assertEqual(self.none_instructor_user_profile.is_instructor, False)

        self.assertTrue(self.instructor_user_profile.activation_token)

    def test_user_activation(self):
        none_instructor_user_profile = self.none_instructor_user_profile
        none_instructor_user_profile.activate_user()
        self.assertEqual(none_instructor_user_profile.user.is_active, True)
        self.assertFalse(none_instructor_user_profile.activation_token)

    def test_sending_email(self):
        instructor_user_profile = self.instructor_user_profile
        self.assertEqual(instructor_user_profile.send_activation_email(), 1)
