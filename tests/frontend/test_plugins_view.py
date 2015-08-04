from django.test import TestCase
from django.contrib.auth.models import User
# from django.core.urlresolvers import reverse
from django.test.client import Client
import responses
import re
import json
import textwrap


class PluginViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'testuser@lisa-project.net', 'testpassword')
        self.plugin_list_json = {
            "test": {
                "name": "lisa-plugins-test",
                "author": "Julien Syx",
                "summary": "Test plugin",
                "version": "0.1.2",
                "repo_url": "https://github.com/Seraf/lisa-plugins-test",
                "keywords": ["test", "debug"]
            }
        }
        self.plugin_changelog = '''
            # v0.1.16
            ## 12/07/2015

            1. [](#new)
            * Adding Changelog file'
        '''

    @responses.activate
    def test_plugins_ok(self):
        url_re = re.compile(
            r'https?://raw.githubusercontent.com/project-lisa/lisa/master/lisa-plugins/lisa-plugins.json'
        )
        responses.add(responses.GET, url_re,
                      body=json.dumps(self.plugin_list_json), status=200,
                      content_type='application/json')

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/plugins/')
        self.assertContains(response, 'Plugins')

    @responses.activate
    def test_plugins_not_found(self):
        url_re = re.compile(
            r'https?://raw.githubusercontent.com/project-lisa/lisa/master/lisa-plugins/lisa-plugins.json'
        )
        responses.add(responses.GET, url_re,
                      body="error", status=404,
                      content_type='application/json')

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/plugins/')
        self.assertContains(response, 'Could not retrieve')

    @responses.activate
    def test_plugins_changelog(self):
        url_re = re.compile(
            r'https?://raw.githubusercontent.com/Seraf/lisa-plugins-test/master/CHANGELOG.md'
        )
        responses.add(responses.GET, url_re,
                      body=textwrap.dedent(self.plugin_changelog).strip(), status=200,
                      content_type='text/markdown')

        session = self.client.session
        session['lisa_all_plugins'] = self.plugin_list_json
        session.save()

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/ajax/plugins/changelog/test')
        self.assertContains(response, '<li><a href="#new"></a></li>')
