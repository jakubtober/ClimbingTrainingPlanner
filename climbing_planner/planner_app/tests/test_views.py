from django.test import TestCase, Client
from django.contrib.auth.models import User


class TestViews(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(username='user', password='test', is_active=True)

    def test_welcome_view(self):
        welcome_view_url = 'http://127.0.0.1:8000/'
        response = self.c.get(welcome_view_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'welcome.html')

    def test_logout_view(self):
        logout_view_url = 'http://127.0.0.1:8000/logout/'
        response = self.c.get(logout_view_url)
        self.assertEqual(response.status_code, 302)

    def test_login_view(self):
        # GET
        login_view_url = 'http://127.0.0.1:8000/login/'
        response = self.c.get(login_view_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.c.login(username='user', password='test')
        response = self.c.get(login_view_url)
        self.assertNotEqual(response.status_code, 200)

        # POST
