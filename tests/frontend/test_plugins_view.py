from django.test import TestCase
from django.contrib.auth.models import User
# from django.core.urlresolvers import reverse
from django.test.client import Client
import responses
import re


class PluginViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'testuser@lisa-project.net', 'testpassword')

    @responses.activate
    def test_plugins(self):
        url_re = re.compile(
            r'https?://raw.githubusercontent.com/project-lisa/lisa/master/lisa-plugins/lisa-plugins.json'
        )
        responses.add(responses.GET, url_re,
                      body="""
                      {"test": {"name": "lisa-plugins-test", "author": "Julien Syx", "summary": "Test plugin",
                      "version": "0.1.2", "repo_url": "https://github.com/Seraf/lisa-plugins-test",
                      "keywords": ["test", "debug"]}}
                      """, status=200,
                      content_type='application/json')

        self.client.login(username='testuser', password='testpassword')
        # Should mock the plugin list and inject a custom plugin to see if it display correctly
        response = self.client.get('/plugins/')
        self.assertContains(response, 'Plugins')
