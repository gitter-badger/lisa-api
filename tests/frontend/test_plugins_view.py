from django.test import TestCase
from django.contrib.auth.models import User
# from django.core.urlresolvers import reverse
from django.test.client import Client


class PluginViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'testuser@lisa-project.net', 'testpassword')

    def test_plugins(self):
        self.client.login(username='testuser', password='testpassword')
        # Should mock the plugin list and inject a custom plugin to see if it display correctly
        response = self.client.get('/plugins/')
        self.assertContains(response, 'Plugins')
