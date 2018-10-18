from django.test import TestCase, Client
from django.contrib.auth.models import User


class TestViews(TestCase):

    def setUp(self):
        self.username = 'user@user.pl'
        self.password = 'test'
        self.c = Client()
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            is_active=True
        )

    def test_welcome_view(self):
        welcome_view_url = 'http://127.0.0.1:8000/'
        response = self.c.get(welcome_view_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'welcome.html')

    def test_logout_view(self):
        # pure GET
        logout_view_url = 'http://127.0.0.1:8000/logout/'
        response = self.c.get(logout_view_url)
        self.assertEqual(response.status_code, 302)

    def test_login_view(self):
        # pure GET
        login_view_url = 'http://127.0.0.1:8000/login/'
        response = self.c.get(login_view_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        # log user in, check if redirects to home
        self.c.login(username=self.username, password=self.password)
        response = self.c.get(login_view_url)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/home/')

        # POST with correct login credentials
        self.c.logout()
        response = self.c.post(
            login_view_url, {
            'username': self.username,
            'password': self.password,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/home/')
        self.assertNotIn('errorlist nonfield', str(response.content))

        # check if redirects to /home/ when user logged
        response = self.c.post(login_view_url, {})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/home/')

        # check using wrong credentials
        # not an email pattern
        self.c.logout()
        response = self.c.post(login_view_url, {
            'username': 'user',
            'password': self.password,
        })
        self.assertIn('errorlist nonfield', str(response.content))

        # not correct password
        self.c.logout()
        response = self.c.post(login_view_url, {
            'username': self.username,
            'password': 'pass',
        })
        self.assertIn('errorlist nonfield', str(response.content))

    def test_logout_view(self):
        logout_view_url = 'http://127.0.0.1:8000/logout/'

        response = self.c.get(logout_view_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/')

        response = self.c.post(logout_view_url, {})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/')

    def test_register_view(self):
        register_view_url = 'http://127.0.0.1:8000/register/'

        response = self.c.get(register_view_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

        # check if user is logged
        self.c.login(username=self.username, password=self.password)
        response = self.c.get(register_view_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/home/')
