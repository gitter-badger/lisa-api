from rest_framework import status
from rest_framework.test import APITestCase
from lisa_api.api.models import Plugin
from lisa_api.lisa.plugin_manager import PluginManager
from django.core.management import call_command, ManagementUtility
from django.test import TestCase
from django.utils.six import StringIO
from django.test.utils import captured_stderr
from testfixtures import log_capture
import mock
import pip


class fakecookie(object):
    class main():
        def cookiecutter():
            raise NotImplementedError


class CommandPluginTest(TestCase):
    @mock.patch('lisa_api.api.management.commands.plugins.cookiecutter')
    def test_command_plugin_output(self, mock_cookiecutter):
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
        self.plugin_url = '/api/v1/core/plugins/%s/' % self.plugin.name
        self.plugin_manager = PluginManager()

    @mock.patch.object(pip, 'main')
    def test_v1_create_plugin(self, mock_pip_main):
        """
        Ensure we can install a new plugin
        """
        url = '/api/v1/core/plugins/'
        data = {
            'name': u'shopping',
            'version': u'1.8.3'
        }
        response = self.client.post(url, data, format='json')
        mock_pip_main.assert_called_once_with(['install', 'lisa-plugins-' + ''.join([data.get('name'), "==",
                                                                                     data.get('version')])])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('name'), data.get('name'))

    @mock.patch.object(pip, 'main')
    def test_v1_destroy_plugin(self, mock_pip_main):
        """
        Ensure we can uninstall a plugin
        """
        response = self.client.delete(self.plugin_url, format='json')
        mock_pip_main.assert_called_once_with(['uninstall', '--yes', 'lisa-plugins-' + self.plugin.name])
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @mock.patch.object(pip, 'main')
    def test_v1_modify_plugin(self, mock_pip_main):
        """
        Ensure we can modify a plugin
        """
        data = {
            'name': u'testplugin',
            'version': u'1.0'
        }
        response = self.client.put(self.plugin_url, data, format='json')
        mock_pip_main.assert_called_once_with(['install', 'lisa-plugins-' + ''.join([data.get('name'), "==",
                                                                                     data.get('version')])])
        self.assertEqual(response.data.get('version'), data.get('version'))

    @log_capture()
    def test_v1_load_intent_plugin(self, l):
        """
        Load plugin intents
        """
        self.plugin_manager.load_intents()
        l.check(
            ('lisa_api', 'INFO', 'There is no plugin loaded')
        )

    @log_capture()
    def test_v1_get_version_plugin(self, l):
        """
        Load plugin version
        """
        version = self.plugin_manager.get_version(plugin_name='shopping')
        # As we don't have plugin loaded, it should use the
        # default value of the base class which is None
        self.assertEqual(version, None)
