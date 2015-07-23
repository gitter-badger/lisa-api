from django.test import TestCase
from django.contrib.auth.models import User
# from django.core.urlresolvers import reverse
from django.test.client import Client


class DashboardViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'testuser@lisa-project.net', 'testpassword')

    def test_dashboard(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/dashboard/')
        self.assertContains(response, 'Dashboard')
