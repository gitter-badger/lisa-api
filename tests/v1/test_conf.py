import mock
from lisa_api.lisa import configuration
from django.core.management import call_command, ManagementUtility
from django.test import TestCase
from django.utils.six import StringIO
from django.test.utils import captured_stderr
from django.conf import settings


class CommandConfTest(TestCase):
    def test_command_configuration_output(self):
        out = StringIO()
        call_command('configuration',
                     '--save',
                     '--filename',
                     settings.BASE_DIR + '/lisa_api.ini',
                     stdout=out)
        self.assertIn('Successfully saved the configuration', out.getvalue())

    def test_command_configuration_error(self):
        with captured_stderr() as stderr, self.assertRaises(SystemExit):
            ManagementUtility(['lisa-api-cli.py', 'configuration']).execute()
        self.assertIn("CommandError", stderr.getvalue())


class ConfTest(TestCase):
    def setUp(self):
        super(ConfTest, self).setUp()
        # We need to reset the CONF object for each test
        self.CONF = configuration.Config()

    def test_init(self):
        config = configuration.Config()
        self.assertTrue(config.parser)
        self.assertTrue(isinstance(config.parser,
                                   configuration.configparser.SafeConfigParser))

    def test_global(self):
        self.assertTrue(configuration.CONF.parser)
        self.assertTrue(isinstance(configuration.CONF, configuration.Config))

    @mock.patch.object(configuration.Config, '_populate_cache')
    @mock.patch.object(configuration.configparser.SafeConfigParser, 'read')
    def test_load(self, mock_read, mock_pop_cache):
        self.CONF.load(settings.BASE_DIR + '/lisa_api.ini')
        self.assertTrue(settings.BASE_DIR + '/lisa_api.ini', self.CONF._filename)
        mock_read.assert_called_once_with(settings.BASE_DIR + '/lisa_api.ini')
        mock_pop_cache.assert_called_once_with()

    @mock.patch.object(configuration.configparser.SafeConfigParser, 'write')
    def test_save_with_filename(self, mock_write):
        m = mock.mock_open()
        with mock.patch('six.moves.builtins.open', m, create=True):
            self.CONF.add_opt(name='test', value='test', section='test')
            self.CONF.save(settings.BASE_DIR + '/lisa_api.ini')
            m.assert_called_once_with(settings.BASE_DIR + '/lisa_api.ini', 'wb')
            mock_write.assert_called_once_with(m())

    def test_add_opt_no_section(self):
        self.CONF.add_opt('fake', 'val')
        self.assertTrue({'fake': 'val'}, self.CONF.parser.defaults())

    def test_add_opt_cast_val_to_string(self):
        self.CONF.add_opt('fakeint', 1)
        self.assertTrue({'fake': 'val', 'fakeint': '1'},
                        self.CONF.parser.defaults())

    def test_add_opt_with_section(self):
        self.assertFalse(self.CONF.parser.has_section('sect'))
        self.CONF.add_opt('fake', 'val', section='sect')
        self.assertTrue(self.CONF.parser.has_section('sect'))
        self.assertEqual('val', self.CONF.parser.get('sect', 'fake'))

    def test_object_attributes(self):
        self.CONF.add_opt('fake1', 'val1')
        self.CONF.add_opt('fake2', 'val2', section='sect1')

        self.assertEqual('val1', self.CONF.fake1)
        self.assertEqual('val2', self.CONF.sect1.fake2)

        self.assertRaises(AttributeError, getattr, self.CONF, 'wrong')
