from rest_framework import status
from rest_framework.test import APITestCase
from lisa_api.api.models import Plugin


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
            'name': u'shopping'
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
