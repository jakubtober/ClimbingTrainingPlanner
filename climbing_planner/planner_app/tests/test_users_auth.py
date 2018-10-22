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

        # create active user
        self.active_user = User.objects.create_user(
            username=active_user_name,
            password=active_user_password,
            is_active=True
        )
        # create not active user
        self.inactive_user = User.objects.create_user(
            username=inactive_user_name,
            password=inactive_user_password,
            is_active=False
        )
        # create profile that is instructor with auth_token
        self.instructor_user_profile = Profile.objects.create(
            user=self.active_user,
            is_instructor=True,
            auth_token=default_token_generator.make_token(self.active_user)
        )
        # create profile that is not an instructor without auth_token
        self.none_instructor_user_profile = Profile.objects.create(
            user=self.inactive_user,
            is_instructor=False
        )

    def test_user_creation(self):
        # creating random users and testing if values are correct
        self.assertEqual(self.active_user.username, 'test1@test.com')
        self.assertEqual(self.active_user.is_active, True)

        self.assertEqual(self.inactive_user.username, 'test2@test.com')
        self.assertEqual(self.inactive_user.is_active, False)

        self.assertEqual(self.instructor_user_profile.user, self.active_user)
        self.assertEqual(self.none_instructor_user_profile.user, self.inactive_user)

        self.assertEqual(self.instructor_user_profile.is_instructor, True)
        self.assertEqual(self.none_instructor_user_profile.is_instructor, False)

        self.assertTrue(self.instructor_user_profile.auth_token)

        test_user = User.objects.create_user(username='test')
        test_profile = Profile.objects.create(user=test_user)
        self.assertTrue(isinstance(test_profile, Profile))
        self.assertEqual(test_profile.__str__(), test_profile.user.username)
        self.assertTrue(test_profile.__str__())

    def test_generating_auth_token(self):
        # get user without auth_token, check if auth_token is false
        # then generate token and check if auth_token exists
        none_instructor_user_profile = self.none_instructor_user_profile
        self.assertFalse(self.none_instructor_user_profile.auth_token)
        none_instructor_user_profile.generate_auth_token()
        self.assertTrue(self.none_instructor_user_profile.auth_token)

    def test_check_auth_token(self):
        token_to_check = self.instructor_user_profile.auth_token
        profile_to_check = self.instructor_user_profile
        self.assertTrue(profile_to_check.check_token(token_to_check))

    def test_user_activation(self):
        # set user to non active
        # then activate and check if it has been activated
        none_instructor_user_profile = self.none_instructor_user_profile
        none_instructor_user_profile.user.is_active = False
        self.assertFalse(self.none_instructor_user_profile.user.is_active)
        none_instructor_user_profile.activate_user()
        self.assertEqual(none_instructor_user_profile.user.is_active, True)
        self.assertFalse(none_instructor_user_profile.auth_token)

    def test_sending_activation_email(self):
        # send activation email and check if function returned True
        # True means email has been sent
        instructor_user_profile = self.instructor_user_profile
        self.assertEqual(instructor_user_profile.send_activation_email(), True)

    def test_sending_reset_password_email(self):
        profile = self.instructor_user_profile
        self.assertTrue(profile.send_reset_password_email())
