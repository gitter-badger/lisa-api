from rest_framework import status
from rest_framework.test import APITestCase
from lisa_api.api.models import Plugin
from django.core.management import call_command, ManagementUtility
from django.test import TestCase
from django.utils.six import StringIO
from django.test.utils import captured_stderr
from cookiecutter import main as cookiecutter
import mock
import sys

class CommandPluginTest(TestCase):
    @mock.patch('cookiecutter.main.cookiecutter')
    @mock.patch('sys.stdin')
    def test_command_plugin_output(self, mock_cookiecutter, mock_stdin):
        out = StringIO()
        call_command('plugins',
                     '--create',
                     stdout=out)
        mock_cookiecutter.assert_called_once_with('https://github.com/project-lisa/cookiecutter-lisa-plugins.git')
        self.assertIn('Successfully created the plugin', out.getvalue())

    def test_command_plugin_error(self):
        with captured_stderr() as stderr, self.assertRaises(SystemExit):
            ManagementUtility(['lisa-api-cli.py', 'plugins']).execute()
        self.assertIn("CommandError", stderr.getvalue())


class CoreTests(APITestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.plugin = Plugin.objects.create(name="testplugin")
        self.plugin_url = '/api/v1/core/plugins/%i/' % self.plugin.id

    def test_v1_create_plugin(self):
        """
        Ensure we can install a new plugin
        """
        url = '/api/v1/core/plugins/'
        data = {
            'name': u'shopping',
            'version': u'1.8.3'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('name'), data.get('name'))

    def test_v1_destroy_plugin(self):
        """
        Ensure we can uninstall a plugin
        """
        response = self.client.delete(self.plugin_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
